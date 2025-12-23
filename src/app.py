from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    url_for,
    session,
    redirect,
    send_file,
)
from flask_bcrypt import Bcrypt
from supabase import create_client, Client
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import timedelta
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask_cors import CORS


# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
load_dotenv()
app = Flask(__name__, template_folder=".", static_folder="static")
CORS(app,supports_credentials=True,origins=["https://web-crawler-mu.vercel.app"])
bcrypt = Bcrypt(app)

app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True  # change to True on production (HTTPS)

PORT = os.getenv("PORT") or 8000
API_KEY = os.getenv("API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase and Gemini
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def crawl_and_extract(url):
    """Fetch webpage and extract title + text content"""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        res = requests.get(url, timeout=10, headers=headers)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "Untitled Page"

        for script in soup(["script", "style"]):
            script.decompose()

        text = " ".join(soup.stripped_strings)
        text = text[:8000]  # limit for Gemini
        return text, title

    except Exception as e:
        return f"Error crawling URL: {e}", "Error"


# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------
@app.route("/api/history")
def api_history():
    user_email = session.get("user_email")
    if not user_email:
        return jsonify({"error": "Unauthorized"}), 401

    results = (
        supabase.table("crawl_results")
        .select("*")
        .eq("user_email", user_email)
        .order("created_at", desc=True)
        .execute()
    )

    # Group by batch_id
    batches = {}
    for item in results.data:
        if item.get("raw_text") is None:
            item["raw_text"] = ""
        batch_id = item.get("batch_id")
        if batch_id:
            if batch_id not in batches:
                batches[batch_id] = {
                    "batch_id": batch_id,
                    "created_at": item["created_at"],
                    "results": [],
                }
            batches[batch_id]["results"].append(item)
        else:
            # Handle legacy single crawls as batches with one item
            single_batch_id = f"single-{item['id']}"
            batches[single_batch_id] = {
                "batch_id": single_batch_id,
                "created_at": item["created_at"],
                "results": [item],
            }

    # Sort batches by created_at desc
    sorted_batches = sorted(
        batches.values(), key=lambda x: x["created_at"], reverse=True
    )

    return jsonify({"batches": sorted_batches})


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/")
def index():
    return render_template("index.html")


# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        existing = supabase.table("users").select("*").eq("email", email).execute()
        if existing.data:
            return jsonify({"error": "User already exists"}), 400

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        supabase.table("users").insert(
            {"email": email, "password": hashed_pw}
        ).execute()
        return jsonify({"message": "Signup successful!"})

    return render_template("signup.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        res = supabase.table("users").select("*").eq("email", email).execute()
        if not res.data:
            return jsonify({"error": "User not found"}), 401

        user = res.data[0]
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid password"}), 401

        # Store email-based session
        session["user_email"] = user["email"]
        return jsonify({"message": "Login successful!"})

    return render_template("login.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    user_email = session.get("user_email")
    if not user_email:
        return redirect(url_for("login"))

    results = (
        supabase.table("crawl_results")
        .select("*")
        .eq("user_email", user_email)
        .order("created_at", desc=True)
        .execute()
    )

    for item in results.data:
        if item.get("raw_text") is None:
            item["raw_text"] = ""

    return render_template("dashboard.html", results=results.data)


# ---------- CRAWL ----------
@app.route("/crawl", methods=["POST"])
def crawl():
    user_email = session.get("user_email")
    if not user_email:
        return jsonify({"error": "Unauthorized. Please log in first."}), 401

    data = request.get_json(silent=True) or {}
    urls = data.get("urls", [])

    if not urls or not isinstance(urls, list):
        return jsonify({"error": "URLs must be provided as a list"}), 400

    batch_id = str(uuid.uuid4())

    def process_url(url):
        text, title = crawl_and_extract(url)
        if text.startswith("Error"):
            return {"url": url, "error": text}

        prompt = f"""
        The following web page content has been extracted:
        ---
        {text}
        ---
        1️⃣ Give me a short descriptive title for the page.
        2️⃣ Summarize it in 5 concise bullet points.
        3️⃣ Extract 5 key entities (people, companies, topics) and list under "Key Entities:".
        Format:
        Title: <short title>
        Summary:
        - ...
        Key Entities:
        - ...
        """

        try:
            response = model.generate_content(prompt)
            ai_output = response.text
        except Exception as e:
            ai_output = f"AI Processing Error: {e}"

        supabase.table("crawl_results").insert(
            {
                "user_email": user_email,
                "batch_id": batch_id,
                "url": url,
                "title": title,
                "summary": ai_output,
                "raw_text": text,
            }
        ).execute()

        return {"url": url, "title": title, "summary": ai_output}

    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_url, url) for url in urls]
        for future in as_completed(futures):
            results.append(future.result())

    return jsonify({"batch_id": batch_id, "results": results})


# ---------- DOWNLOAD PDF ----------
@app.route("/download/pdf", methods=["POST"])
def download_pdf():
    user_email = session.get("user_email")
    if not user_email:
        return jsonify({"error": "Unauthorized. Please log in first."}), 401

    data = request.get_json()
    summary = data.get("summary", "")
    url = data.get("url", "")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(50, 800, "WebCrawler Report")
    pdf.drawString(50, 780, f"URL: {url}")

    pdf.drawString(50, 750, "Summary:")
    text_obj = pdf.beginText(50, 730)
    for line in summary.split("\n"):
        text_obj.textLine(line)

    pdf.drawText(text_obj)
    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="crawl_report.pdf",
        mimetype="application/pdf",
    )


# ---------- DOWNLOAD BATCH PDF ----------
@app.route("/download/batch/pdf", methods=["POST"])
def download_batch_pdf():
    user_email = session.get("user_email")
    if not user_email:
        return jsonify({"error": "Unauthorized. Please log in first."}), 401

    data = request.get_json()
    batch_id = data.get("batch_id", "")

    # Fetch batch results
    results = (
        supabase.table("crawl_results")
        .select("*")
        .eq("user_email", user_email)
        .eq("batch_id", batch_id)
        .execute()
    )

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    def draw_wrapped_text(pdf, text, x, y, max_width, line_height=14):
        """Draw text with word wrapping"""
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if pdf.stringWidth(test_line, "Helvetica", 10) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    y = height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, f"WebCrawler Batch Report")
    y -= 30
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Batch ID: {batch_id}")
    y -= 40

    for item in results.data:
        if y < 150:  # Check if we need a new page
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(50, y, f"WebCrawler Batch Report (continued)")
            y -= 30
            pdf.setFont("Helvetica", 12)
            pdf.drawString(50, y, f"Batch ID: {batch_id}")
            y -= 40

        # URL
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "URL:")
        y -= 15
        pdf.setFont("Helvetica", 10)
        url_lines = draw_wrapped_text(pdf, item["url"], 50, y, width - 100)
        for line in url_lines:
            pdf.drawString(70, y, line)
            y -= 14
        y -= 5

        # Title
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Title:")
        y -= 15
        pdf.setFont("Helvetica", 10)
        title_lines = draw_wrapped_text(
            pdf, item["title"] or "Untitled Page", 50, y, width - 100
        )
        for line in title_lines:
            pdf.drawString(70, y, line)
            y -= 14
        y -= 10

        # Summary
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Summary:")
        y -= 15
        pdf.setFont("Helvetica", 10)
        summary_lines = draw_wrapped_text(pdf, item["summary"], 50, y, width - 100)
        for line in summary_lines:
            if y < 50:  # Check for page break in middle of summary
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(50, y, "Summary (continued):")
                y -= 15
                pdf.setFont("Helvetica", 10)
            pdf.drawString(70, y, line)
            y -= 14
        y -= 20  # Space between items

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="batch_crawl_report.pdf",
        mimetype="application/pdf",
    )


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=int(PORT))

@app.route("/api/auth/status")
def auth_status():
    if session.get("user_email"):
        return jsonify({"authenticated": True})
    return jsonify({"authenticated": False}), 401
# ---------------------------------------------------
from flask import Flask, render_template, request, jsonify, url_for, session, redirect
from flask_bcrypt import Bcrypt
from supabase import create_client, Client
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import timedelta
# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
load_dotenv()
<<<<<<< HEAD
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False  # change to True on production (HTTPS)
=======
PORT = int(os.getenv("PORT", 8080))

# Initialize Flask
app = Flask(__name__,template_folder="templates",static_folder="static")

# === Configure Gemini securely ===
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("❌  GEMINI_API_KEY environment variable not set")
>>>>>>> 3bf385e541334f778ef97361a05958672a8f829e

PORT = os.getenv("PORT") or 8000
<<<<<<< HEAD
API_KEY = os.getenv("API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase and Gemini
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=API_KEY)
=======
API_KEY = os.getenv("API_KEY") or ""
# Configure Gemini API
genai.configure(api_key=api_key)
>>>>>>> 3bf385e541334f778ef97361a05958672a8f829e
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
@app.route("/history")
def history():
    user_email = session.get("user_email")
    if not user_email:
        return redirect(url_for("login"))  # redirect instead of raw JSON

    results = (
        supabase.table("crawl_results")
        .select("*")
        .eq("user_email", user_email)
        .order("created_at", desc=True)
        .execute()
    )

    # Prevent crash on None values
    for item in results.data:
        if item.get("raw_text") is None:
            item["raw_text"] = ""

    return render_template("history.html", results=results.data)

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
        supabase.table("users").insert({"email": email, "password": hashed_pw}).execute()
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
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    text, title = crawl_and_extract(url)
    if text.startswith("Error"):
        return jsonify({"error": text}), 400

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

    supabase.table("crawl_results").insert({
        "user_email": user_email,
        "url": url,
        "title": title,
        "summary": ai_output,
        "raw_text": text
    }).execute()

    return jsonify({
        "title": title,
        "summary": ai_output,
        "url": url
    })

# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=int(PORT))

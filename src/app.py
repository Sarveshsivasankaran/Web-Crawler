from flask import Flask, render_template, request, jsonify,url_for
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Load environment variables
PORT = os.getenv("PORT") or 8000
API_KEY = os.getenv("API_KEY") or ""
print(API_KEY)
# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


def crawl_and_extract(url):
    """Fetch webpage and extract text content"""
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
        for script in soup(["script", "style"]):
            script.decompose()

        text = " ".join(soup.stripped_strings)
        return text[:8000]  # Trim to avoid token overload
    except requests.exceptions.RequestException as e:
        return f"Error crawling URL: Request failed ({e})"
    except Exception as e:
        return f"Error crawling URL: An unexpected error occurred ({e})"


# ---------- ROUTES ---------- #

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/crawl", methods=["POST"])
def crawl():
    data = request.get_json(silent=True) or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    text = crawl_and_extract(url)

    if "Error crawling URL" in text:
        return jsonify({"error": text}), 400

    prompt = f"""
    Summarize the following web page in 5 concise bullet points.
    Also extract 5 key entities (like people, companies, topics) and list them under a separate heading 'Key Entities:'.
    Content:
    {text}
    """

    try:
        response = model.generate_content(prompt)
        ai_output = response.text
    except Exception as e:
        ai_output = f"AI Processing Error: {e}"

    return jsonify({"summary": ai_output})


if __name__ == "__main__":
    app.run(debug=True, port=int(PORT))
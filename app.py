from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import os

# Initialize Flask
app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-2.5-flash")

def crawl_and_extract(url):
    """Fetch webpage and extract text content"""
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = ' '.join(soup.stripped_strings)
        return text[:8000]  # Trim to avoid token overload
    except Exception as e:
        return f"Error crawling URL: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crawl", methods=["POST"])
def crawl():
    data = request.get_json()
    url = data.get("url")
    text = crawl_and_extract(url)

    if text.startswith("Error"):
        return jsonify({"error": text}), 400

    prompt = f"""
    Summarize the following web page in 5 bullet points.
    Also extract 5 key entities (like people, companies, topics).
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
    app.run(debug=True)
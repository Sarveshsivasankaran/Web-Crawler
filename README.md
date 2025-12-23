<h1>🕷️ WebCrawler | Levellers</h1>
<p>
  <strong>AI-Powered Intelligent Web Crawling & Insight Extraction</strong><br>
  Built under the <strong>Codesapines Mentorship Program</strong>
</p>

<hr>

<h2>🚀 Overview</h2>
<p>
  <strong>WebCrawler</strong> is an AI-driven web crawling and insight extraction platform that integrates
  <strong>Google Gemini AI</strong> with a full-stack Flask application.
  It intelligently crawls webpages, extracts structured content, generates summaries,
  identifies key entities, and stores user-specific crawl history using <strong>Supabase</strong>.
</p>

<p>
  Developed by <strong>Team Levellers</strong> — Sarvesh, Sejal, Priyans
</p>

<hr>

<h2>✅ Features</h2>

<h3>🧠 Core Intelligence</h3>
<ul>
  <li>AI-powered webpage summarization using <strong>Gemini 2.5 Flash</strong></li>
  <li>Key entity extraction (people, companies, topics)</li>
  <li>Smart text extraction using <strong>BeautifulSoup</strong></li>
  <li>Handles JavaScript-heavy and modern web pages</li>
</ul>

<h3>🔐 Authentication & Sessions</h3>
<ul>
  <li>Redesigned <strong>Login</strong> & <strong>Signup</strong> pages</li>
  <li>Secure password hashing using <strong>Flask-Bcrypt</strong></li>
  <li>Session-based authentication with Flask sessions</li>
  <li>User-specific access control for crawling & downloads</li>
</ul>

<h3>🗄️ Database & Storage</h3>
<ul>
  <li>Supabase PostgreSQL backend</li>
  <li>Stores user credentials (hashed)</li>
  <li>Stores crawl results, summaries, URLs, batch IDs, timestamps</li>
</ul>

<h3>📊 Dashboard</h3>
<ul>
  <li>Redesigned dashboard UI</li>
  <li>Single URL & batch URL crawling</li>
  <li>Displays AI-generated summaries & extracted entities</li>
  <li>User-specific crawl history</li>
</ul>

<h3>📥 Reports & Downloads</h3>
<ul>
  <li>Download crawl results as <strong>PDF reports</strong></li>
  <li>Batch crawl PDF report generation</li>
  <li>Formatted, readable multi-page PDF output</li>
</ul>

<hr>

<h2>🏛️ Architecture</h2>

<pre>
Frontend (HTML, CSS, JS)
        |
        v
Flask Backend (Python)
        |
        +--> Supabase (PostgreSQL Database)
        |
        +--> Gemini AI (Summaries & Entity Extraction)
        |
        +--> Crawler Engine (Requests + BeautifulSoup)
</pre>

<hr>

<h2>🧠 Tech Stack</h2>

<h3>Frontend</h3>
<ul>
  <li>HTML5, CSS3</li>
  <li>Vanilla JavaScript</li>
  <li>Responsive UI</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Python + Flask</li>
  <li>Flask-Bcrypt</li>
  <li>Flask Sessions</li>
  <li>BeautifulSoup4</li>
  <li>Requests</li>
</ul>

<h3>AI Layer</h3>
<ul>
  <li>Google Gemini <strong>(gemini-2.5-flash)</strong></li>
</ul>

<h3>Database</h3>
<ul>
  <li>Supabase</li>
  <li>PostgreSQL</li>
</ul>

<hr>

<h2>📦 Installation</h2>

<h3>1️⃣ Clone Repository</h3>
<pre><code>git clone https://github.com/yourusername/WebCrawler.git
cd WebCrawler
</code></pre>

<h3>2️⃣ Install Dependencies</h3>
<pre><code>pip install -r requirements.txt
</code></pre>

<h3>3️⃣ Create <code>.env</code> File</h3>
<pre><code>API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key
SECRET_KEY=your_flask_secret
</code></pre>

<h3>4️⃣ Run Server</h3>
<pre><code>python app.py
</code></pre>

<hr>

<h2>🕸️ API Endpoints</h2>

<h3><code>POST /signup</code></h3>
<p>Creates a new user account.</p>

<h3><code>POST /login</code></h3>
<p>Validates credentials and starts a session.</p>

<h3><code>POST /crawl</code></h3>
<p>Accepts a list of URLs and performs batch crawling using Gemini AI.</p>

<h3><code>GET /api/history</code></h3>
<p>Returns user-specific crawl history.</p>

<h3><code>POST /download/pdf</code></h3>
<p>Downloads a single crawl report as PDF.</p>

<h3><code>POST /download/batch/pdf</code></h3>
<p>Downloads a batch crawl report as PDF.</p>

<hr>

<h2>🛠️ Project Structure</h2>

<pre>
WEB-CRAWLER/
│── README.md
│── requirements.txt
│── .gitignore
│
├── src/
│   │── app.py
│   │── .env
│   │
│   ├── static/
│   │    ├── style.css
│   │    ├── script.js
│   │    ├── fonts/
│   │    └── img/
│   │         └── icon.png
│   │
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── history.html
│
└── .dist/
</pre>

<hr>

<h2>👥 Team Members</h2>
<ul>
  <li><a href="https://www.linkedin.com/in/sarvesh-sivasankaran">Sarvesh S</a></li>
  <li><a href="https://www.linkedin.com/in/priyans-raj-bhandara-ab57a4310/">Priyans</a></li>
  <li><a href="https://www.linkedin.com/in/sejal-sai-s-43338132b/">Sejal Sai</a></li>
</ul>

<hr>

<h2>🏆 Codesapines Mentorship</h2>
<p>
  This project was developed under the <strong>Codesapines Mentorship Program</strong>,
  emphasizing real-world problem solving, system design, and production-ready development.
</p>

<hr>

<h2>🔮 Future Enhancements</h2>
<ul>
  <li>JWT-based authentication</li>
  <li>Role-based user access</li>
  <li>CSV export support</li>
  <li>Advanced crawl scheduling</li>
</ul>

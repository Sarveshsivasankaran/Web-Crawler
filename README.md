<h1>🕷️ WebCrawler | Levellers</h1>
<p><strong>AI-Powered Intelligent Web Crawling & Insight Extraction</strong><br>
Built under the <strong>Codesapines Mentorship Program</strong></p>

<hr>

<h2>🚀 Overview</h2>
<p><strong>WebCrawler</strong> is an AI-driven web exploration and data extraction platform that integrates 
<strong>Google Gemini AI</strong> with a full-stack Flask application. It intelligently crawls webpages, extracts structured 
information, generates summaries, identifies key entities, and stores user crawl history through Supabase.</p>

<p>This project is developed by <strong>Team Levellers</strong> — Sejal, Priyans & CODE-O-PHILES.</p>

<hr>

<h2>✅ Features</h2>

<h3>Core System</h3>
<ul>
  <li>AI-powered webpage summarization using <strong>Gemini 1.5 Flash</strong></li>
  <li>Intelligent text extraction using BeautifulSoup</li>
  <li>Entity extraction & insight generation</li>
  <li>Clean and responsive landing page UI</li>
</ul>

<h3>Authentication</h3>
<ul>
  <li>Redesigned <strong>Login</strong> & <strong>Signup</strong> modals</li>
  <li>Fully integrated with <strong>Supabase Auth</strong></li>
  <li>Secure password handling + session management</li>
</ul>

<h3>Database</h3>
<ul>
  <li>Supabase PostgreSQL backend</li>
  <li>Stores user accounts, crawling history, summaries, and timestamps</li>
</ul>

<h3>Dashboard</h3>
<ul>
  <li>Newly redesigned dashboard UI</li>
  <li>Displays AI-generated summaries and extracted entities</li>
  <li>Shows full user crawl history</li>
</ul>

<hr>

<h2>🏛️ Architecture</h2>

<pre>
Frontend (HTML, CSS, JS)
        |
        v
Flask Backend (Python)
        |
        +--> Supabase (Auth + Database)
        |
        +--> Gemini AI (Summaries + Insights)
        |
        +--> Crawler Engine (Requests + BS4)
</pre>

<hr>

<h2>🧠 Tech Stack</h2>

<h3>Frontend</h3>
<ul>
  <li>HTML5, CSS3</li>
  <li>Vanilla JavaScript</li>
  <li>Custom UI Components</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Python + Flask</li>
  <li>BeautifulSoup4</li>
  <li>Requests</li>
</ul>

<h3>AI Layer</h3>
<ul>
  <li>Google Gemini (gemini-1.5-flash)</li>
</ul>

<h3>Database</h3>
<ul>
  <li>Supabase</li>
  <li>PostgreSQL</li>
</ul>

<hr>

<h2>📦 Installation</h2>

<h3>1. Clone Repository</h3>
<pre><code>git clone https://github.com/yourusername/WebCrawler.git
cd WebCrawler
</code></pre>

<h3>2. Install Dependencies</h3>
<pre><code>pip install -r requirements.txt
</code></pre>

<h3>3. Create <code>.env</code> File</h3>
<pre><code>GEMINI_API_KEY=your_gemini_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key
SECRET_KEY=your_flask_secret
</code></pre>

<h3>4. Run Server</h3>
<pre><code>python app.py
</code></pre>

<hr>

<h2>🕸️ API Endpoints</h2>

<h3><code>POST /crawl</code></h3>
<p>Crawls URL + processes via Gemini. Returns:</p>
<pre><code>{
  "summary": "...",
  "entities": [...],
  "url": "...",
  "timestamp": "..."
}
</code></pre>

<h3><code>POST /auth/signup</code></h3>
<p>Creates a new user using Supabase Auth.</p>

<h3><code>POST /auth/login</code></h3>
<p>Validates login credentials + returns session.</p>

<h3><code>GET /history</code></h3>
<p>Returns user-specific crawl logs from Supabase.</p>

<hr>

<h2>📊 Dashboard Features</h2>
<ul>
  <li>URL input console</li>
  <li>Real-time Gemini AI summaries</li>
  <li>Entity extraction</li>
  <li>User-specific crawl history table</li>
</ul>

<hr>

<h2>🛠️ Project Structure</h2>
<pre>
WebCrawler/
│── app.py
│── .env
│── requirements.txt
│── templates/
│     ├── index.html
│     ├── crawl.html
│     └── dashboard.html
│── static/
      ├── style.css
      ├── script.js
      └── img/
</pre>

<hr>

<h2>👥 Team Members</h2>
<ul>
  <li>[Sarvesh S](www.linkedin.com/in/sarvesh-sivasankaran)</li>
  <li>[Priyans](https://www.linkedin.com/in/priyans-raj-bhandara-ab57a4310/)</li>
  <li>[Sejal Sai](https://www.linkedin.com/in/sejal-sai-s-43338132b/)</li>
</ul>

<hr>

<h2>🏆 Codesapines Mentorship</h2>
<p>Developed under the <strong>Codesapines Mentorship Program</strong>, focusing on hands-on, real-world software development.</p>

<hr>

<h2>✅ Future Enhancements</h2>
<ul>
  <li>Batch URL crawling</li>
  <li>Semantic search using vector embeddings</li>
  <li>Role-based user access</li>
  <li>AI-enhanced crawl prioritization</li>
  <li>Downloadable PDF/CSV reports</li>
</ul>

<hr>

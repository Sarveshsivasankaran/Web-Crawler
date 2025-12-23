/* ===============================
   CONFIG
================================ */
const API_BASE = "https://web-crawler-backend-51dl.onrender.com";


/* ===============================
   MODAL ELEMENTS
================================ */
const loginModal = document.getElementById("loginModal");
const signupModal = document.getElementById("signupModal");

const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");

const closeLogin = document.getElementById("closeLogin");
const closeSignup = document.getElementById("closeSignup");


/* ===============================
   OPEN / CLOSE MODALS
================================ */
if (loginBtn)
  loginBtn.onclick = () => (loginModal.style.display = "flex");

if (signupBtn)
  signupBtn.onclick = () => (signupModal.style.display = "flex");

if (closeLogin)
  closeLogin.onclick = () => (loginModal.style.display = "none");

if (closeSignup)
  closeSignup.onclick = () => (signupModal.style.display = "none");

window.onclick = (event) => {
  if (event.target === loginModal) loginModal.style.display = "none";
  if (event.target === signupModal) signupModal.style.display = "none";
};


/* ===============================
   AUTH HELPERS
================================ */
function getToken() {
  return localStorage.getItem("access_token");
}

function isLoggedIn() {
  return !!getToken();
}

function logout() {
  localStorage.removeItem("access_token");
  alert("Logged out successfully");
  window.location.href = "/index.html";
}



/* ===============================
   LOGIN
================================ */
const loginSubmit = document.getElementById("loginSubmit");

if (loginSubmit) {
  loginSubmit.onclick = async () => {
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        credentials: "include", // 🔥 REQUIRED FOR SESSIONS
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Login failed");
        return;
      }

      alert("Login successful!");
      window.location.href = "/dashboard.html";

    } catch (err) {
      alert("🚨 Error connecting to server.");
    }
  };
}


/* ===============================
   SIGNUP
================================ */
const signupSubmit = document.getElementById("signupSubmit");

if (signupSubmit) {
  signupSubmit.onclick = async () => {
    const email = document.getElementById("signupEmail").value.trim();
    const password = document.getElementById("signupPassword").value.trim();

    if (!email || !password) {
      alert("Please fill all fields");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/signup`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Signup failed");
        return;
      }

      alert("Account created successfully. Please login.");
      window.location.href = "/login.html";

    } catch (err) {
      alert("🚨 Error connecting to server.");
    }
  };
}


/* ===============================
   CRAWL (SINGLE URL)
================================ */
const crawlBtn = document.getElementById("crawlBtn");

if (crawlBtn) {
  crawlBtn.onclick = async () => {
    const url = prompt("Enter URL to crawl");
    if (!url) return;

    try {
      const res = await fetch(`${API_BASE}/crawl`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ urls: [url] }) // 🔥 MUST BE LIST
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Crawling failed");
        return;
      }

      document.getElementById("result").innerText =
        JSON.stringify(data.results, null, 2);

    } catch (err) {
      alert("🚨 Error while crawling.");
    }
  };
}


/* ===============================
   BATCH CRAWL
================================ */
const batchCrawlBtn = document.getElementById("batchCrawlBtn");

if (batchCrawlBtn) {
  batchCrawlBtn.onclick = async () => {
    const rawInput = document.getElementById("batchUrls").value;

    const urls = rawInput
      .split("\n")
      .map(u => u.trim())
      .filter(u => u.length > 0);

    if (urls.length === 0) {
      alert("Please enter at least one valid URL.");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/crawl`, {
        method: "POST",
        credentials: "include", // 🔥 REQUIRED FOR FLASK SESSION
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ urls }) // 🔥 BACKEND EXPECTS LIST
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Batch crawl failed");
        return;
      }

      // Display results nicely
      const output = data.results
        .map(r => {
          if (r.error) {
            return `❌ ${r.url}\n${r.error}\n`;
          }
          return `✅ ${r.url}\n${r.summary}\n`;
        })
        .join("\n----------------------\n");

      document.getElementById("batchResult").innerText = output;

    } catch (err) {
      alert("🚨 Error while batch crawling.");
    }
  };
}


/* ===============================
   PDF DOWNLOAD
================================ */
const downloadPDF = document.getElementById("downloadPDF");

if (downloadPDF) {
  downloadPDF.onclick = async () => {
    try {
      const res = await fetch(`${API_BASE}/download/pdf`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          summary: document.getElementById("result").innerText,
          url: "User Crawled URL"
        })
      });

      const blob = await res.blob();
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "crawl_report.pdf";
      link.click();

    } catch (err) {
      alert("🚨 Failed to download PDF");
    }
  };
}


/* ===============================
   AUTO REDIRECT IF LOGGED IN
================================ */
if (window.location.pathname.includes("login")) {
  if (isLoggedIn()) window.location.href = "/dashboard.html";
}
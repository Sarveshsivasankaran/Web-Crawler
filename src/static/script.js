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
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Login failed");
        return;
      }

      localStorage.setItem("access_token", data.token);

      alert("Login successful!");
      loginModal.style.display = "none";
      window.location.href = "/dashboard.html";

    } catch (err) {
      alert("Server error. Please try again.");
    }
  };
}


/* ===============================
   SIGNUP
================================ */
const signupSubmit = document.getElementById("signupSubmit");

if (signupSubmit) {
  signupSubmit.onclick = async () => {
    const name = document.getElementById("signupName").value.trim();
    const email = document.getElementById("signupEmail").value.trim();
    const password = document.getElementById("signupPassword").value.trim();

    if (!name || !email || !password) {
      alert("Please fill all fields");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Signup failed");
        return;
      }

      alert("Account created successfully. Please login.");
      signupModal.style.display = "none";
      loginModal.style.display = "flex";

    } catch (err) {
      alert("Server error. Please try again.");
    }
  };
}


/* ===============================
   CRAWL (SINGLE URL)
================================ */
const crawlBtn = document.getElementById("crawlBtn");

if (crawlBtn) {
  crawlBtn.onclick = async () => {
    if (!isLoggedIn()) {
      loginModal.style.display = "flex";
      return;
    }

    const url = prompt("Enter URL to crawl");
    if (!url) return;

    try {
      const res = await fetch(`${API_BASE}/crawl`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ url })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Crawling failed");
        return;
      }

      document.getElementById("result").innerText = data.summary;

    } catch (err) {
      alert("Error while crawling");
    }
  };
}


/* ===============================
   BATCH CRAWL
================================ */
const batchCrawlBtn = document.getElementById("batchCrawlBtn");

if (batchCrawlBtn) {
  batchCrawlBtn.onclick = async () => {
    const urls = document.getElementById("batchUrls").value
      .split("\n")
      .map(u => u.trim())
      .filter(Boolean);

    if (urls.length === 0) {
      alert("Enter at least one URL");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/batch-crawl`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ urls })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Batch crawl failed");
        return;
      }

      document.getElementById("result").innerText =
        JSON.stringify(data.results, null, 2);

    } catch (err) {
      alert("Server error");
    }
  };
}


/* ===============================
   PDF DOWNLOAD
================================ */
const downloadPDF = document.getElementById("downloadPDF");

if (downloadPDF) {
  downloadPDF.onclick = async () => {
    const res = await fetch(`${API_BASE}/download/pdf`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${getToken()}`
      }
    });

    const blob = await res.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "crawl_report.pdf";
    link.click();
  };
}


/* ===============================
   AUTO REDIRECT IF LOGGED IN
================================ */
if (window.location.pathname.includes("login")) {
  if (isLoggedIn()) window.location.href = "/dashboard.html";
}
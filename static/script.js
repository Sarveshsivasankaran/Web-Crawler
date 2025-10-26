// === Modal Logic ===
const loginModal = document.getElementById("loginModal");
const signupModal = document.getElementById("signupModal");
const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");
const closeLogin = document.getElementById("closeLogin");
const btncrawl = document.getElementById("btncrawl");

loginBtn.onclick = () => loginModal.style.display = "flex";
signupBtn.onclick = () => signupModal.style.display = "flex";
closeLogin.onclick = () => loginModal.style.display = "none";
closeSignup.onclick = () => signupModal.style.display = "none";
btncrawl.onclick = () => signupModal.style.display = "none";

window.onclick = (event) => {
  if (event.target === loginModal) loginModal.style.display = "none";
  if (event.target === signupModal) signupModal.style.display = "none";
};
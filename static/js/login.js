const authCard = document.getElementById("auth-card");
const loginToggle = document.getElementById("login-toggle");
const signupToggle = document.getElementById("signup-toggle");
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");
const sideTitle = document.getElementById("side-title");
const sideSubtitle = document.getElementById("side-subtitle");

function updateSide(title, subtitle) {
  sideTitle.classList.add("title-change");

  setTimeout(() => {
    sideTitle.textContent = title;
    sideSubtitle.textContent = subtitle;
    sideTitle.classList.remove("title-change");
  }, 150);
}

function showLogin() {
  loginToggle.classList.add("active");
  signupToggle.classList.remove("active");

  signupForm.classList.remove("active-form");
  loginForm.classList.add("active-form");

  authCard.classList.replace("register-mode", "login-mode");

  updateSide("Log in.", "Welcome back, farmer.");
}

function showRegister() {
  signupToggle.classList.add("active");
  loginToggle.classList.remove("active");

  loginForm.classList.remove("active-form");
  signupForm.classList.add("active-form");

  authCard.classList.replace("login-mode", "register-mode");

  updateSide("Register.", "Start your journey with us.");
}

loginToggle.addEventListener("click", showLogin);
signupToggle.addEventListener("click", showRegister);

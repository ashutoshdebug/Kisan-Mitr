// console.log("File attached")
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

// Warning message
loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);
  formData.append("form_type", "login_form");
  fetch("/login", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      const contentType = response.headers.get("content-type");
      // Login failed:
      // Flask returned {"not_exist": true}
      if (contentType && contentType.includes("application/json")) {
        return response.json();
      }
      // Login successful:
      // Flask redirected to /upload
      window.location.href = response.url;
      return null;
    })
    .then((data) => {
      if (!data) {
        return;
      }
      if (data.not_exist === true) {
        const warning_login = document.getElementById("warning-login");
        warning_login.textContent = "Invalid email or password.";
        warning_login.style.display = "block";
        warning_login.style.color = "red";
      }
    })
    .catch((error) => {
      console.error("Login error:", error);
    });
});

signupForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData_signup = new FormData(signupForm);
  formData_signup.append("form_type", "signup_form");
  fetch("/login", {
    method: "POST",
    body: formData_signup,
  })
    .then((response) => {
      const contentType = response.headers.get("content-type");
      // Login failed:
      // Flask returned {"not_exist": true}
      if (contentType && contentType.includes("application/json")) {
        return response.json();
      }
      // Login successful:
      // Flask redirected to /upload
      window.location.href = response.url;
      return null;
    })
    .then((data) => {
      if (!data) {
        return;
      }
      if (data.user_already_exist === true) {
        const warning_signup = document.getElementById("warning-signup");
        warning_signup.textContent = "User already exist!";
        warning_signup.style.display = "block";
        warning_signup.style.color = "red";
      }
    })
    .catch((error) => {
      console.error("Login error:", error);
    });
});

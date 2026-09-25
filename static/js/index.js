const scroll = new LocomotiveScroll({
  el: document.querySelector("[data-scroll-container]"),
  smooth: true,
});

const accountMenu = document.querySelector("#account-menu");
const accountButton = document.querySelector("#account-button");
const dropDown = document.querySelector(".logout-dropdown");
const logoutBtn = document.querySelector("#logout-btn");

let hideTimeout;

const showDropdown = () => {
  clearTimeout(hideTimeout);
  dropDown?.classList.add("logout-dropdown-show");
};

const hideDropdown = () => {
  hideTimeout = setTimeout(() => {
    dropDown?.classList.remove("logout-dropdown-show");
  }, 180);
};

if (accountMenu && dropDown) {
  accountMenu.addEventListener("mouseenter", showDropdown);
  accountMenu.addEventListener("mouseleave", hideDropdown);
  dropDown.addEventListener("mouseenter", showDropdown);
  dropDown.addEventListener("mouseleave", hideDropdown);
}

if (accountButton && dropDown) {
  accountButton.addEventListener("click", (event) => {
    event.stopPropagation();
    clearTimeout(hideTimeout);
    dropDown.classList.toggle("logout-dropdown-show");
  });
}

document.addEventListener("click", (event) => {
  if (accountMenu && !accountMenu.contains(event.target)) {
    dropDown?.classList.remove("logout-dropdown-show");
  }
});

if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    try {
      const response = await fetch("/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          logout: true,
        }),
      });

      if (!response.ok) {
        throw new Error("Logout failed");
      }

      window.location.href = "/";

    } catch (error) {
      console.error("Logout error:", error);
    }
  });
}
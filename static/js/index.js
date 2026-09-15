const scroll = new LocomotiveScroll({
  el: document.querySelector("[data-scroll-container]"),
  smooth: true,
});

const accountMenu = document.querySelector("#account-menu");
const dropDown = document.querySelector(".logout-dropdown");
const logoutBtn = document.querySelector("#logout-btn");

let hideTimeout;

const showDropdown = () => {
  clearTimeout(hideTimeout);

  if (!dropDown) return;

  dropDown.classList.add("logout-dropdown-show");
};

const hideDropdown = () => {
  hideTimeout = setTimeout(() => {
    if (!dropDown) return;

    dropDown.classList.remove("logout-dropdown-show");
  }, 200);
};

if (accountMenu && dropDown) {
  accountMenu.addEventListener("mouseenter", showDropdown);
  accountMenu.addEventListener("mouseleave", hideDropdown);

  dropDown.addEventListener("mouseenter", showDropdown);
  dropDown.addEventListener("mouseleave", hideDropdown);
}

if (logoutBtn) {
  logoutBtn.addEventListener("click", async (event) => {
    event.preventDefault();

    console.log("Log out button clicked");

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
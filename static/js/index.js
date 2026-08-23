const scroll = new LocomotiveScroll({
  el: document.querySelector("[data-scroll-container]"),
  smooth: true,
});

const accountMenu = document.querySelector("#account-menu");
const dropDown = document.querySelector(".logout-dropdown");

let hideTimeout;
// let logOutbtn = false;

const showDropdown = () => {
  clearTimeout(hideTimeout);
  dropDown.classList.add("logout-dropdown-show");
};

const hideDropdown = () => {
  hideTimeout = setTimeout(() => {
    dropDown.classList.remove("logout-dropdown-show");
  }, 200);
};

accountMenu.addEventListener("mouseenter", showDropdown);
accountMenu.addEventListener("mouseleave", hideDropdown);

dropDown.addEventListener("mouseenter", showDropdown);
dropDown.addEventListener("mouseleave", hideDropdown);

dropDown.addEventListener("click", () => {
  console.log('Log out button clicked')
  const logOutbtn = true;
  const payload = {logout: logOutbtn};

  fetch("/logout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
})
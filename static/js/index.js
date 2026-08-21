// Locomotive scroll
const scroll = new LocomotiveScroll({
  el: document.querySelector("[data-scroll-container]"),
  smooth: true,
});

const accountMenu = document.querySelector("#account-menu");
const dropDown = document.querySelector(".logout-dropdown");

accountMenu.addEventListener("mouseenter", () => {
  // console.log('ENTER');
  dropDown.classList.add("logout-dropdown-show");
});

accountMenu.addEventListener("mouseleave", () => {
  // console.log('LEAVE');
  dropDown.classList.remove("logout-dropdown-show");
});

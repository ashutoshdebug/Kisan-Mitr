/* =========================================================
   LOCOMOTIVE SCROLL
   ========================================================= */

const scrollContainer =
  document.querySelector("[data-scroll-container]");

let scroll = null;

if (
  scrollContainer &&
  typeof LocomotiveScroll !== "undefined"
) {
  scroll = new LocomotiveScroll({
    el: scrollContainer,
    smooth: true,
  });
}


/* =========================================================
   ELEMENTS
   ========================================================= */

const navbar =
  document.querySelector("#navbar");

const accountMenu =
  document.querySelector("#account-menu");

const accountButton =
  document.querySelector("#account-button");

const dropDown =
  document.querySelector(".logout-dropdown");

const logoutBtn =
  document.querySelector("#logout-btn");


/* =========================================================
   ACCOUNT DROPDOWN
   ========================================================= */

let hideTimeout;

const showDropdown = () => {

  clearTimeout(hideTimeout);

  if (dropDown) {
    dropDown.classList.add(
      "logout-dropdown-show"
    );
  }
};


const hideDropdown = () => {

  hideTimeout = setTimeout(() => {

    if (dropDown) {
      dropDown.classList.remove(
        "logout-dropdown-show"
      );
    }

  }, 180);
};


if (accountMenu && dropDown) {

  accountMenu.addEventListener(
    "mouseenter",
    showDropdown
  );

  accountMenu.addEventListener(
    "mouseleave",
    hideDropdown
  );

  dropDown.addEventListener(
    "mouseenter",
    showDropdown
  );

  dropDown.addEventListener(
    "mouseleave",
    hideDropdown
  );
}


if (accountButton && dropDown) {

  accountButton.addEventListener(
    "click",
    (event) => {

      event.stopPropagation();

      clearTimeout(hideTimeout);

      dropDown.classList.toggle(
        "logout-dropdown-show"
      );
    }
  );
}


document.addEventListener(
  "click",
  (event) => {

    if (
      accountMenu &&
      !accountMenu.contains(event.target)
    ) {

      dropDown?.classList.remove(
        "logout-dropdown-show"
      );
    }
  }
);


/* =========================================================
   LOGOUT
   ========================================================= */

if (logoutBtn) {

  logoutBtn.addEventListener(
    "click",
    async () => {

      try {

        const response = await fetch(
          "/logout",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              logout: true,
            }),
          }
        );

        if (!response.ok) {
          throw new Error(
            "Logout failed"
          );
        }

        window.location.href = "/";

      } catch (error) {

        console.error(
          "Logout error:",
          error
        );
      }
    }
  );
}


/* =========================================================
   NAVBAR SCROLL
   ========================================================= */

/*
   0 - 20px
   Full navbar

   20 - 60px
   Previous state maintained
   This prevents flickering

   60px+
   Glass capsule
*/

const TOP_THRESHOLD = 20;
const CAPSULE_THRESHOLD = 60;

let navbarIsScrolled = false;
let ticking = false;


const updateNavbar = () => {

  if (!navbar) {
    ticking = false;
    return;
  }

  const currentScroll =
    window.scrollY ||
    window.pageYOffset ||
    0;


  /* =========================
     FULL NAVBAR
     ========================= */

  if (
    currentScroll <= TOP_THRESHOLD &&
    navbarIsScrolled
  ) {

    navbarIsScrolled = false;

    navbar.classList.remove(
      "navbar-scrolled"
    );

    navbar.classList.remove(
      "navbar-hidden"
    );
  }


  /* =========================
     GLASS CAPSULE
     ========================= */

  else if (
    currentScroll >= CAPSULE_THRESHOLD &&
    !navbarIsScrolled
  ) {

    navbarIsScrolled = true;

    navbar.classList.add(
      "navbar-scrolled"
    );

    navbar.classList.remove(
      "navbar-hidden"
    );

    /* Close account dropdown
       when navbar becomes capsule */

    if (dropDown) {
      dropDown.classList.remove(
        "logout-dropdown-show"
      );
    }
  }


  ticking = false;
};


/* =========================================================
   SCROLL EVENT
   ========================================================= */

window.addEventListener(
  "scroll",
  () => {

    if (!ticking) {

      window.requestAnimationFrame(
        updateNavbar
      );

      ticking = true;
    }

  },
  {
    passive: true,
  }
);


/* =========================================================
   INITIAL STATE
   ========================================================= */

updateNavbar();
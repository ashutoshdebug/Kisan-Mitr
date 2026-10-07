// ========================================
// LOCOMOTIVE SCROLL
// ========================================

const scrollContainer = document.querySelector(
  "[data-scroll-container]"
);

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


// ========================================
// ACCOUNT DROPDOWN
// ========================================

const accountMenu = document.querySelector(
  "#account-menu"
);

const accountButton = document.querySelector(
  "#account-button"
);

const dropDown = document.querySelector(
  ".logout-dropdown"
);

const logoutBtn = document.querySelector(
  "#logout-btn"
);

let hideTimeout;


const showDropdown = () => {

  clearTimeout(hideTimeout);

  dropDown?.classList.add(
    "logout-dropdown-show"
  );
};


const hideDropdown = () => {

  hideTimeout = setTimeout(() => {

    dropDown?.classList.remove(
      "logout-dropdown-show"
    );

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


// ========================================
// NAVBAR SCROLL BEHAVIOUR
// ========================================

const navbar = document.querySelector(
  "#navbar"
);


// ------------------------------------------------
// IMPORTANT THRESHOLDS
// ------------------------------------------------
//
// FULL NAVBAR:
// 0 - 20px
//
// CAPSULE:
// 60px+
//
// BETWEEN 20px AND 60px:
// Keep current state.
//
// This gap prevents flickering.
// ------------------------------------------------

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
    window.scrollY || window.pageYOffset;


  // ======================================
  // RETURN TO FULL NAVBAR
  // ======================================

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


  // ======================================
  // CHANGE TO CAPSULE
  // ======================================

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


    // Close account dropdown
    dropDown?.classList.remove(
      "logout-dropdown-show"
    );
  }


  ticking = false;
};


// ========================================
// SCROLL LISTENER
// ========================================

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
    passive: true
  }
);


// ========================================
// INITIAL NAVBAR STATE
// ========================================

updateNavbar();


// ========================================
// LOGOUT
// ========================================

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

      }

      catch (error) {

        console.error(
          "Logout error:",
          error
        );

      }

    }
  );

}
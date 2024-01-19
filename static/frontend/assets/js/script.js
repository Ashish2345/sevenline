let hamBtn = document.querySelector(".hamburger__icon");
let mobileMenu = document.querySelector(".header__nav-bottom .nav__menu");

if (mobileMenu && hamBtn) {
  hamBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("active");
  });
}
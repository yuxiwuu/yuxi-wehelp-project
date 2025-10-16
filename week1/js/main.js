const burger = document.querySelector(".burger");
const mobileNav = document.querySelector(".mobile_nav");

burger.addEventListener("click", () => {
  burger.classList.toggle("isOpen");
  mobileNav.classList.toggle("isOpen");
});

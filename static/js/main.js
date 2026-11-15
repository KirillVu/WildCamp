const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector("#main-nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const opened = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(opened));
  });
}

// Панель фильтров каталога на экранах уже 1200 px
const filtersForm = document.querySelector("#filters");
const filtersToggle = document.querySelector(".filters-toggle");
if (filtersForm && filtersToggle) {
  filtersToggle.addEventListener("click", () => {
    const opened = filtersForm.classList.toggle("is-open");
    filtersToggle.setAttribute("aria-expanded", String(opened));
  });
}

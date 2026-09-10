"use strict";

document.documentElement.classList.add("js");

const header = document.querySelector("[data-header]");
const menuToggle = document.querySelector("[data-menu-toggle]");
const mobileNav = document.querySelector("[data-mobile-nav]");
const contactForm = document.querySelector("[data-contact-form]");
const formNote = document.querySelector("[data-form-note]");
const yearNode = document.querySelector("[data-current-year]");

if (yearNode) {
  yearNode.textContent = String(new Date().getFullYear());
}

const updateHeader = () => {
  if (!header) return;
  header.classList.toggle("scrolled", window.scrollY > 18);
};

updateHeader();
window.addEventListener("scroll", updateHeader, { passive: true });

const closeMenu = () => {
  if (!menuToggle || !mobileNav || !header) return;
  menuToggle.setAttribute("aria-expanded", "false");
  menuToggle.setAttribute("aria-label", "Abrir menu");
  mobileNav.hidden = true;
  header.classList.remove("menu-active");
  document.body.classList.remove("menu-open");
};

const openMenu = () => {
  if (!menuToggle || !mobileNav || !header) return;
  menuToggle.setAttribute("aria-expanded", "true");
  menuToggle.setAttribute("aria-label", "Fechar menu");
  mobileNav.hidden = false;
  header.classList.add("menu-active");
  document.body.classList.add("menu-open");
};

if (menuToggle && mobileNav) {
  menuToggle.addEventListener("click", () => {
    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
    if (isOpen) closeMenu();
    else openMenu();
  });

  mobileNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeMenu();
      menuToggle.focus();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 880) closeMenu();
  });
}

const revealItems = document.querySelectorAll(".reveal");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (reducedMotion || !("IntersectionObserver" in window)) {
  revealItems.forEach((item) => item.classList.add("is-visible"));
} else {
  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -8%", threshold: 0.08 },
  );

  revealItems.forEach((item) => revealObserver.observe(item));
}

if (contactForm instanceof HTMLFormElement) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!contactForm.checkValidity()) {
      contactForm.reportValidity();
      if (formNote) formNote.textContent = "Confira os campos destacados antes de continuar.";
      return;
    }

    const data = new FormData(contactForm);
    const name = String(data.get("name") || "").trim();
    const business = String(data.get("business") || "").trim();
    const segment = String(data.get("segment") || "").trim();
    const message = String(data.get("message") || "").trim();

    const lines = [
      "Olá! Vim pelo site da VOLTTA System e gostaria de solicitar uma demonstração.",
      "",
      `Nome: ${name}`,
      business ? `Negócio: ${business}` : null,
      `Segmento: ${segment}`,
      `Objetivo: ${message}`,
    ].filter(Boolean);

    const whatsappUrl = new URL("https://wa.me/5582991880566");
    whatsappUrl.searchParams.set("text", lines.join("\n"));

    if (formNote) formNote.textContent = "Abrindo o WhatsApp para concluir seu contato…";
    window.open(whatsappUrl.toString(), "_blank", "noopener,noreferrer");
  });
}

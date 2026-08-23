// ============================================================
// GEMEINSAMES NAVIGATIONS-VERHALTEN
// Wird von allen Seiten eingebunden, die den gemeinsamen Header
// (templates/header.html) verwenden.
//
// - Sprachumschalter (Language Switcher)
// - Mobile Navigation (Hamburger-Menü)
// - Navbar-Hintergrund beim Scrollen
// ============================================================

const htmlEl           = document.documentElement;
const langOptions      = document.querySelectorAll('.lang-option');
const currentLangLabel = document.getElementById('current-lang-label');
const langSwitcherBtn  = document.querySelector('.lang-switcher-btn');
const langDropdown     = document.querySelector('.lang-dropdown');

// Sprache aus localStorage laden (falls vorhanden)
const savedLang = localStorage.getItem('wedding-lang');
if (savedLang && (savedLang === 'de' || savedLang === 'it')) {
  setLanguage(savedLang);
}

function setLanguage(lang) {
  // 1. data-lang auf <html> setzen — CSS kümmert sich um den Rest
  htmlEl.setAttribute('data-lang', lang);
  htmlEl.setAttribute('lang', lang === 'de' ? 'de-CH' : 'it');

  // 2. Label im Dropdown-Button aktualisieren
  if (currentLangLabel) currentLangLabel.textContent = lang.toUpperCase();

  // 3. Platzhalter in Formularfeldern aktualisieren
  document.querySelectorAll('[data-placeholder-' + lang + ']').forEach(el => {
    el.placeholder = el.getAttribute('data-placeholder-' + lang);
  });

  // 4. In localStorage speichern
  localStorage.setItem('wedding-lang', lang);
}

// Klick auf eine Sprach-Option
langOptions.forEach(option => {
  option.addEventListener('click', () => {
    setLanguage(option.getAttribute('data-lang'));
    langDropdown.classList.remove('lang-dropdown-open');
    langSwitcherBtn.setAttribute('aria-expanded', 'false');
  });
});

// Dropdown öffnen/schliessen
if (langSwitcherBtn) {
  langSwitcherBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = langDropdown.classList.toggle('lang-dropdown-open');
    langSwitcherBtn.setAttribute('aria-expanded', isOpen);
  });
}

// Dropdown schliessen, wenn ausserhalb geklickt wird
document.addEventListener('click', () => {
  if (langDropdown) langDropdown.classList.remove('lang-dropdown-open');
  if (langSwitcherBtn) langSwitcherBtn.setAttribute('aria-expanded', 'false');
});


// ---- MOBILE NAVIGATION (Hamburger-Menü) ----
const navToggle = document.querySelector('.nav-toggle');
const navLinks  = document.querySelector('.nav-links');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('nav-open');
    navToggle.classList.toggle('active');
    navToggle.setAttribute('aria-expanded', isOpen);
  });

  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('nav-open');
      navToggle.classList.remove('active');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}


// ---- NAVBAR: Hintergrund bei Scroll ----
// Seiten ohne Hero-Bild rendern die Navbar serverseitig bereits im
// "scrolled"-Stil (data-static-navbar) — dort braucht es keinen
// Scroll-Listener, der die Klasse wieder entfernen könnte.
const navbar = document.getElementById('navbar');
if (navbar && navbar.dataset.staticNavbar !== 'true') {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  });
}

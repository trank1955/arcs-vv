// menu.js: inietta menu responsive unico (desktop + mobile) in #menu-inject

(function() {
  // Determina se siamo nella vera root (solo / o /index.html), altrimenti sempre sottocartella
  var isRoot = window.location.pathname.replace(/\\/g, '/').match(/^\/?(index\.html)?$/);
  // Usa sempre la cartella 'pages' (non 'pagine') dalla root
  var prefix = isRoot ? 'pages/' : '';
  var iconPrefix = isRoot ? 'icons/' : '../icons/';

  // Voci di menu
  var menuItems = [
    { href: prefix + 'index.html', icon: iconPrefix + 'home-icon.svg', label: 'Home' },
    { href: prefix + 'attivita.html', icon: iconPrefix + 'attivita-icon.svg', label: 'Attività' },
    { href: prefix + 'chi-siamo.html', icon: iconPrefix + 'chi-siamo-icon.svg', label: 'Chi siamo' },
    { href: prefix + 'dove-siamo.html', icon: iconPrefix + 'dove-siamo-icon.svg', label: 'Dove siamo' },
    { href: prefix + 'news.html', icon: iconPrefix + 'news-icon.svg', label: 'News' },
    { href: prefix + 'assistente.html', icon: iconPrefix + 'assistente-icon.svg', label: 'Assistente' },
    { href: prefix + 'contatti.html', icon: iconPrefix + 'contatti-icon.svg', label: 'Contatti' },
    { href: prefix + 'iscriviti.html', icon: iconPrefix + 'iscriviti-icon.svg', label: 'Iscriviti' },
    { href: prefix + 'donazioni.html', icon: iconPrefix + 'donazioni-icon.svg', label: 'Donazioni' }
  ];

  // Desktop menu
  var desktopMenu = '<nav class="desktop-menu"><div style="display:flex;align-items:center;gap:2em;width:100%;">';
  desktopMenu += '<span class="menu-logo-title" style="display:flex;align-items:center;gap:0.5em;line-height:1.1;">';
  desktopMenu += '<img src="' + iconPrefix + 'logo-cuore.png" alt="Logo ARCS-VV" style="height:32px;width:32px;vertical-align:middle;">';
  desktopMenu += '<span style="color:#fff;font-size:0.95em;line-height:1.1;font-weight:bold;">Associazione Rete di Cittadinanza Solidale</span>';
  desktopMenu += '</span>';
  desktopMenu += '<ul style="display:flex;gap:1em;list-style:none;align-items:center;margin:0;">';
  menuItems.forEach(function(item) {
    desktopMenu += '<li><a href="' + item.href + '"><img src="' + item.icon + '" class="menu-icon" alt="' + item.label + '">' + item.label + '</a></li>';
  });
  desktopMenu += '</ul></div></nav>';

  // Mobile menu
  var mobileMenu = '<div class="mobile-menu-trigger" id="mobileMenuTrigger" aria-label="Apri menu" tabindex="0"><span></span><span></span><span></span></div>';
  mobileMenu += '<div class="mobile-menu-overlay" id="mobileMenuOverlay"></div>';
  mobileMenu += '<nav class="mobile-menu" id="mobileMenu">';
  menuItems.forEach(function(item) {
    mobileMenu += '<a href="' + item.href + '">' + item.label + '</a>';
  });
  mobileMenu += '</nav>';

  // CSS inline
  var menuCSS = `<style>
    nav.desktop-menu { display: flex; }
    .mobile-menu-trigger { display: none; }
    @media (max-width: 900px) {
      nav.desktop-menu { display: none !important; }
      .mobile-menu-trigger { display: flex !important; }
    }
    .mobile-menu-overlay {
      display: none;
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0,0,0,0.4); z-index: 9998;
    }
    .mobile-menu {
      display: none;
      position: fixed; top: 0; right: 0; width: 80vw; max-width: 320px; height: 100vh;
      background: #8b4513; color: #fff; z-index: 9999; box-shadow: -4px 0 24px rgba(0,0,0,0.18);
      flex-direction: column; padding: 2em 1em;
    }
    .mobile-menu.open, .mobile-menu-overlay.open { display: flex !important; }
    .mobile-menu a { color: #fff; text-decoration: none; font-size: 1.2em; margin: 1em 0; }
    .mobile-menu-trigger {
      position: fixed; top: 14px; right: 14px; z-index: 10000;
      width: 38px; height: 38px; background: var(--mobile-accent, #1565c0); border-radius: 8px;
      flex-direction: column; justify-content: center; align-items: center; cursor: pointer;
      box-shadow: 0 2px 8px rgba(21,101,192,0.12);
      transition: background 0.2s;
    }
    .mobile-menu-trigger span {
      display: block; width: 20px; height: 3px; background: #fff; margin: 3px 0; border-radius: 2px;
      transition: background 0.2s;
    }
    .mobile-menu-trigger:active, .mobile-menu-trigger:focus {
      background: var(--mobile-nav, #8b4513);
    }
  </style>`;

  var menuHTML = desktopMenu + mobileMenu + menuCSS;
  var container = document.getElementById('menu-inject');
  if(container) container.innerHTML = menuHTML;

  // Mobile menu logic
  var trigger = document.getElementById('mobileMenuTrigger');
  var menu = document.getElementById('mobileMenu');
  var overlay = document.getElementById('mobileMenuOverlay');
  if(trigger && menu && overlay) {
    function openMenu() {
      menu.classList.add('open');
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function closeMenu() {
      menu.classList.remove('open');
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }
    function toggleMenu() {
      if(menu.classList.contains('open')) {
        closeMenu();
      } else {
        openMenu();
      }
    }
    trigger.addEventListener('click', toggleMenu);
    overlay.addEventListener('click', closeMenu);
    menu.querySelectorAll('a').forEach(function(link){ link.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function(e){ if(e.key==='Escape') closeMenu(); });
  }
})();

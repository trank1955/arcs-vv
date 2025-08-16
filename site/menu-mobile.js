
// INSERIMENTO HAMBURGER MENU MOBILE MINIMALE

window.addEventListener('DOMContentLoaded', function() {
  // Crea hamburger
  const hamburger = document.createElement('div');
  hamburger.id = 'hamburger-menu';
  hamburger.setAttribute('aria-label', 'Apri menu di navigazione');
  hamburger.setAttribute('tabindex', '0');
  hamburger.style.position = 'fixed';
  hamburger.style.top = '20px';
  hamburger.style.right = '20px';
  hamburger.style.width = '50px';
  hamburger.style.height = '50px';
  // Sfondo adattivo: usa variabile CSS se presente, fallback blu
  let bgColor = getComputedStyle(document.body).getPropertyValue('--mobile-nav').trim() || '#2980b9';
  // Modalità scura: hamburger chiaro
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    bgColor = '#fff';
  }
  hamburger.style.background = bgColor;
  hamburger.style.color = (bgColor === '#fff' ? '#2980b9' : '#fff');
  hamburger.style.borderRadius = '10px';
  hamburger.style.zIndex = '10001';
  hamburger.style.display = 'flex';
  hamburger.style.flexDirection = 'column';
  hamburger.style.justifyContent = 'center';
  hamburger.style.alignItems = 'center';
  hamburger.style.cursor = 'pointer';
  hamburger.style.transition = 'box-shadow 0.2s';
  // Hover effect
  hamburger.addEventListener('mouseenter', function() {
    hamburger.style.boxShadow = '0 0 0 4px #2980b988';
  });
  hamburger.addEventListener('mouseleave', function() {
    hamburger.style.boxShadow = '';
  });
  hamburger.addEventListener('mousedown', function() {
    hamburger.style.opacity = '0.7';
  });
  hamburger.addEventListener('mouseup', function() {
    hamburger.style.opacity = '1';
  });
  // Icona hamburger (3 linee)
  for (let i = 0; i < 3; i++) {
    const bar = document.createElement('div');
    bar.style.width = '30px';
    bar.style.height = '5px';
  bar.style.background = (bgColor === '#fff' ? '#2980b9' : '#fff');
    bar.style.margin = '4px 0';
    bar.style.borderRadius = '2px';
    hamburger.appendChild(bar);
  }
  document.body.appendChild(hamburger);

  // Crea menu mobile
  const mobileMenu = document.createElement('div');
  mobileMenu.id = 'mobile-menu';
  mobileMenu.style.position = 'fixed';
  mobileMenu.style.top = '0';
  mobileMenu.style.right = '0';
  mobileMenu.style.width = '70vw';
  mobileMenu.style.maxWidth = '320px';
  mobileMenu.style.height = '100vh';
  mobileMenu.style.background = '#fff';
  mobileMenu.style.boxShadow = '-4px 0 24px rgba(0,0,0,0.25)';
  mobileMenu.style.zIndex = '10000';
  mobileMenu.style.transform = 'translateX(100%)';
  mobileMenu.style.transition = 'transform 0.3s cubic-bezier(.77,0,.18,1)';
  // Calcola prefisso percorso
  mobileMenu.innerHTML = '<ul style="list-style:none;padding:2em 1em;font-size:1.2em;">'
    +'<li><a href="/index.html">Home</a></li>'
    +'<li><a href="/pagine/attivita.html">Attività</a></li>'
    +'<li><a href="/pagine/chi-siamo.html">Chi siamo</a></li>'
    +'<li><a href="/pagine/dove-siamo.html">Dove siamo</a></li>'
    +'<li><a href="/pagine/news.html">News</a></li>'
    +'<li><a href="/pagine/contatti.html">Contatti</a></li>'
    +'<li><a href="/pagine/iscriviti.html">Iscriviti</a></li>'
    +'<li><a href="/pagine/donazioni.html">Donazioni</a></li>'
    +'</ul>';
  document.body.appendChild(mobileMenu);

  // Overlay
  const overlay = document.createElement('div');
  overlay.id = 'menu-overlay';
  overlay.style.position = 'fixed';
  overlay.style.top = '0';
  overlay.style.left = '0';
  overlay.style.width = '100vw';
  overlay.style.height = '100vh';
  overlay.style.background = 'rgba(0,0,0,0.45)';
  overlay.style.zIndex = '9999';
  overlay.style.display = 'none';
  overlay.style.transition = 'background 0.3s';
  document.body.appendChild(overlay);

  // Apertura menu
  function openMenu() {
    mobileMenu.style.transform = 'translateX(0)';
    overlay.style.display = 'block';
    setTimeout(() => { overlay.style.background = 'rgba(0,0,0,0.45)'; }, 10);
    document.body.style.overflow = 'hidden';
  }
  // Chiusura menu
  function closeMenu() {
    mobileMenu.style.transform = 'translateX(100%)';
    overlay.style.background = 'rgba(0,0,0,0)';
    setTimeout(() => { overlay.style.display = 'none'; }, 300);
    document.body.style.overflow = '';
  }
  hamburger.addEventListener('click', openMenu);
  overlay.addEventListener('click', closeMenu);
  // Chiudi menu su click link
  mobileMenu.addEventListener('click', function(e) {
    if (e.target.tagName === 'A') closeMenu();
  });
  // Chiudi menu su ESC
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeMenu();
  });
  // Accessibilità: apri menu con Enter/Space
  hamburger.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' || e.key === ' ') openMenu();
  });
});

(function() {
  // Determina il prefisso corretto per le icone e i link in base al path
  let iconPrefix = "icons/";
  let homeLink = "index.html";
  let attivitaLink = "pagine/attivita.html";
  let chiSiamoLink = "pagine/chi-siamo.html";
  let doveSiamoLink = "pagine/dove-siamo.html";
  let newsLink = "pagine/news.html";
  let statutoLink = "pagine/statuto.html";
  let contattiLink = "pagine/contatti.html";
  let iscrivitiLink = "pagine/iscriviti.html";
  let donazioniLink = "pagine/donazioni.html";
  const path = window.location.pathname;
    if (path.includes("index-mobile.html")) {
      iconPrefix = "icons/";
      homeLink = "index-mobile.html";
      attivitaLink = "pagine/attivita-mobile.html";
      chiSiamoLink = "pagine/chi-siamo-mobile.html";
      doveSiamoLink = "pagine/dove-siamo-mobile.html";
      newsLink = "pagine/news-mobile.html";
      statutoLink = "pagine/statuto-mobile.html";
      contattiLink = "pagine/contatti-mobile.html";
      iscrivitiLink = "pagine/iscriviti-mobile.html";
      donazioniLink = "pagine/donazioni-mobile.html";
  } else if (path.includes("/pagine/")) {
    iconPrefix = "../icons/";
    homeLink = "../index.html";
    attivitaLink = "attivita.html";
    chiSiamoLink = "chi-siamo.html";
    doveSiamoLink = "dove-siamo.html";
    newsLink = "news.html";
    statutoLink = "statuto.html";
    contattiLink = "contatti.html";
    iscrivitiLink = "iscriviti.html";
    donazioniLink = "donazioni.html";
  }

  const menuHTML = `
    <nav style="display:flex;align-items:center;justify-content:space-between;width:100%;padding:0.5em 1em 0.5em 0.5em;box-sizing:border-box;">
      <div class="logo-container" style="display:flex;align-items:center;gap:0.5em;">
        <a href="${homeLink}"><img src="${iconPrefix}favicon.ico" alt="Logo ARCS-VV" class="logo"></a>
        <span class="logo-title">ARCS-VV</span>
      </div>
      <div class="hamburger-menu" aria-label="Apri menu" tabindex="0" style="margin-left:auto;">
        <div class="hamburger-line"></div>
        <div class="hamburger-line"></div>
        <div class="hamburger-line"></div>
      </div>
      <ul style="display:none;"></ul>
    </nav>
    <div class="mobile-menu-overlay"></div>
    <nav class="mobile-menu">
      <ul>
        <li><a href="${homeLink}"><img src="${iconPrefix}home-icon.svg" alt="Home" class="menu-icon"> Home</a></li>
        <li><a href="${attivitaLink}"><img src="${iconPrefix}attivita-icon.svg" alt="Attività" class="menu-icon"> Attività</a></li>
        <li><a href="${chiSiamoLink}"><img src="${iconPrefix}chi-siamo-icon.svg" alt="Chi siamo" class="menu-icon"> Chi siamo</a></li>
        <li><a href="${doveSiamoLink}"><img src="${iconPrefix}dove-siamo-icon.svg" alt="Dove siamo" class="menu-icon"> Dove siamo</a></li>
        <li><a href="${newsLink}"><img src="${iconPrefix}news-icon.svg" alt="News" class="menu-icon"> News</a></li>
        <li><a href="${statutoLink}"><img src="${iconPrefix}statuto-icon.svg" alt="Statuto" class="menu-icon"> Statuto</a></li>
        <li><a href="${contattiLink}"><img src="${iconPrefix}contatti-icon.svg" alt="Contatti" class="menu-icon"> Contatti</a></li>
        <li><a href="${iscrivitiLink}"><img src="${iconPrefix}iscriviti-icon.svg" alt="Iscriviti" class="menu-icon"> Iscriviti</a></li>
        <li><a href="${donazioniLink}"><img src="${iconPrefix}donazioni-icon.svg" alt="Donazioni" class="menu-icon"> Donazioni</a></li>
      </ul>
    </nav>
  `;

  document.addEventListener('DOMContentLoaded', function() {
    document.body.insertAdjacentHTML('afterbegin', menuHTML);
    console.log('[menu-mobile.js] menuHTML inserito');

    // Logica hamburger per mobile
    const hamburger = document.querySelector('.hamburger-menu');
    const mobileMenu = document.querySelector('.mobile-menu');
    const overlay = document.querySelector('.mobile-menu-overlay');

    console.log('[menu-mobile.js] hamburger:', hamburger);
    console.log('[menu-mobile.js] mobileMenu:', mobileMenu);
    console.log('[menu-mobile.js] overlay:', overlay);

    if (hamburger && mobileMenu && overlay) {
      // Forza sfondo e colore icone per visibilità
      mobileMenu.style.background = '#2980b9'; // blu visibile
      const icons = mobileMenu.querySelectorAll('img.menu-icon');
      icons.forEach(icon => { icon.style.filter = 'brightness(0) invert(1)'; });
      function openMenu() {
        console.log('[menu-mobile.js] openMenu chiamato');
        hamburger.classList.add('active');
        mobileMenu.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
      function closeMenu() {
        console.log('[menu-mobile.js] closeMenu chiamato');
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }
      hamburger.addEventListener('click', function() {
        console.log('[menu-mobile.js] hamburger click');
        openMenu();
      });
      hamburger.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          console.log('[menu-mobile.js] hamburger keydown', e.key);
          openMenu();
        }
      });
      overlay.addEventListener('click', function() {
        console.log('[menu-mobile.js] overlay click');
        closeMenu();
      });
      mobileMenu.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
          console.log('[menu-mobile.js] mobileMenu link click', e.target.href);
          closeMenu();
        }
      });
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          console.log('[menu-mobile.js] ESC keydown');
          closeMenu();
        }
      });
    } else {
      console.warn('[menu-mobile.js] Elementi menu non trovati!');
    }
  });
})();

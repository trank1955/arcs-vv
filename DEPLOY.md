Deploy del sito

Contenuto da pubblicare
- Cartella `public/` contiene solo i file destinati alla pubblicazione:
  - `index.html`, `main.css`, `menu.js`
  - `icons/`, `immagini/`, `pages/`

Come pubblicare
- Carica l'intera cartella `public/` sul server (document root) o sincronizzala con il provider di hosting.
- Se il server usa come document root la root del progetto, punta invece la root a `public/`.

Note
- Il codice e i materiali di lavoro sono sotto `dev/` e non vanno online.
- Le pagine News sono ora dinamiche:
  - Lista: `public/pages/news.html` legge `public/pages/news/news.json` e mostra le card in griglia 2×.
  - Dettaglio: `public/pages/news_post.html?slug=...` apre il singolo articolo, sempre da `news.json`.
  - Non serve più generare i singoli HTML dei post in `public/`.
  - Se in `news.json` il campo `content` contiene HTML completo (menu, script, link “torna alle news”), il dettaglio lo ripulisce automaticamente.

Strumenti
- Tool gestione News (GUI): `tools/blog_manager/blog_manager.py`
  - Avvio rapido: `python3 run_blog_manager.py`
  - Il tool scrive/legge da `pages/news` e `pages/news/news.json`, usa `immagini/` per le immagini, e salva i backup in `pages/news/backups/`.
  - Il file di log si trova accanto al tool (`tools/blog_manager/log_blog_manager.txt`).
  - Per pubblicare le news aggiornate:
    - Comando veloce: `python3 tools/deploy_news.py`
      - Copia `pages/news/news.json` in `public/pages/news/news.json`
      - Copia eventuali `pages/news/*.html` (i singoli post) in `public/pages/news/` per compatibilità con link diretti (non sovrascrive la lista e la pagina dinamica)

- Deploy completo (consigliato): `python3 tools/deploy_all.py`
  - Sincronizza `menu.js` e `main.css` nella `public/`
  - Sincronizza `pages/news.html` e `pages/news_post.html` nella `public/pages/`
  - Esegue il deploy delle news (equivalente a `deploy_news.py`)
  - Copia `icons/`, `immagini/` e `pdf/` dentro `public/`
  - Crea uno ZIP di `public/` pronto per l'upload (`public_dist_YYYYMMDD_HHMMSS.zip`)

## Comandi rapidi

- Aggiorna news: `make news` oppure `./update_news.sh`
- Deploy completo + zip: `make deploy` oppure `./deploy_all.sh`
- Servi in locale la cartella public: `make serve` (porta 8000)
- Pulizia cache/log: `make clean`


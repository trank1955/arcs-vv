Sommario sviluppo e prossimi passi

Struttura progetto
- public/: contenuto pubblicabile (index.html, main.css, menu.js, icons/, immagini/, pages/)
- tools/blog_manager/: Blog Manager GUI per gestire le News
- dev/: materiale non pubblico (backup, template di lavoro, ide/)
- DEPLOY.md: come pubblicare (usa la cartella public/)

<!-- Sezione Assistente rimossa dal progetto -->

Blog Manager (News)
- Avvio: `python3 run_blog_manager.py`
- Percorsi:
  - HTML/JSON: pages/news/
  - Immagini: immagini/
  - Backup: pages/news/backups/
- Pulsanti:
  - Nuovo: crea post con struttura pronta (meta, menu, riassunto, contenuto)
  - Nuovo da template: idem, ma apre subito l’editor
  - Apri cartella News/Immagini: scorciatoie per lavorare sui file
  - Rigenera news.json: allinea news.json leggendo i file HTML

Pulizia fatta
- Rimossi file News di prova e riferimenti "pagine/" errati
- Centralizzato il menu (menu.js) e rimosso il vecchio menu-mobile.js
- Creato public/ per semplificare il deploy; spostato materiale di lavoro in dev/

TODO (prossimi passi)
- Contenuti reali: creare 1–3 news vere con titolo, data, riassunto e (opzionale) immagine
- SEO: opzionale, permettere slug personalizzato in Blog Manager
- Grafica: rifinire stile chat per aderire ancor più a main.css
- Deploy: verificare che l’hosting punti a public/ oppure caricare solo public/

Comandi utili
- Avvio Blog Manager: `python3 run_blog_manager.py`
- Rigenera news.json (GUI): dal pulsante "Rigenera news.json"
- Validazione rapida link (linux/mac): `rg -n "href=\"pagine/|/pagine/|main.js" -S public` (nessun risultato atteso)

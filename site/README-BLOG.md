# ARCS-VV – Gestione News/Blog

Questo README spiega come gestire le news del sito e come creare l'eseguibile Windows del Blog Manager.

## Struttura
- templates/: template Jinja2 condivisi
- pages/: pagine generate del sito
  - news/: pagine dettaglio dei post + news.json
- immagini/, icons/, main.css: asset condivisi

## Flusso operativo (semplice)
1) Modifica/aggiungi/elimina post con il Blog Manager (Windows):
   - Avvia `ArcsBlogManager.exe` dalla cartella radice del sito.
   - Il programma legge/scrive `pages/news/news.json` e rigenera automaticamente:
     - `pages/news.html` (elenco, 2 colonne, responsive)
     - `pages/news/<slug>.html` (dettagli)

2) Alternativa CLI (multi-piattaforma):
   - Normalizza dati (facoltativo):
     - `python pages/news/dev/normalize_news_json.py`
   - Genera sito base:
     - `python dev/genera_sito.py` (rigenera tutte le pagine principali)
   - Genera pagina News + dettagli:
     - `python pages/news/dev/genera_news.py`

## Note sui contenuti
- I post sono in `pages/news/news.json`.
- Campi supportati: `title`, `slug`, `date` (YYYY-MM-DD), `author`, `excerpt`, `content` (HTML), `youtube` (lista URL), `pdf` (lista nomi file).
- Immagini: se `post.image` è un path relativo (es. `immagini/banner.jpg`), il template lo risolve; se è già `../immagini/...` o un URL, viene usato così.

## Build Windows (EXE)
Prerequisiti: Python 3.10+ su Windows, pip.

1) (Opzionale) Crea virtualenv ed installa dipendenze:
```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

2) Compila l’eseguibile:
```
cd pages\news\dev
build_windows.bat
```
Output: `pages\news\dev\dist\ArcsBlogManager.exe`

3) Uso dell’eseguibile:
- Copia `ArcsBlogManager.exe` nella radice del sito (insieme a `templates/`, `pages/`, `immagini/`, `icons/`, `main.css`).
- Avvialo con doppio click.

## Consigli
- Mantieni `news.json` ordinato e con date in formato YYYY-MM-DD.
- Evita di incollare intere pagine HTML nel campo `content`; inserisci solo il corpo dell’articolo.
- Per PDF, copia i file in `pages/news/pdf/` e metti i nomi nel campo `pdf`.
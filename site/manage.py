#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import shutil
import webbrowser
from pathlib import Path

# Importa percorsi centralizzati
try:
    from pages.news.dev.config_paths import BASE_DIR, PAGES_DIR, NEWS_DIR, NEWS_JSON_PATH, TEMPLATES_DIR
except Exception as e:
    print("[ERRORE] Impossibile caricare config_paths:", e)
    print("Assicurati di lanciare questo script dalla radice del sito (dove ci sono 'templates' e 'pages').")
    sys.exit(1)


def run_script(script_rel_path: Path, input_text: str | None = None, attach: bool = False) -> int:
    """Esegue uno script Python relativo alla radice del sito.
    - attach=True: collega lo stdin/stdout della console (per modalità interattive)
    - input_text: invia input testuale allo script (per saltare prompt)
    """
    script_path = (BASE_DIR / script_rel_path).resolve()
    if not script_path.exists():
        print(f"[ERRORE] Script non trovato: {script_path}")
        return 1
    try:
        if attach and input_text is None:
            return subprocess.call([sys.executable, str(script_path)])
        res = subprocess.run([sys.executable, str(script_path)], input=input_text, text=True, capture_output=True)
        if res.stdout:
            print(res.stdout)
        if res.stderr:
            print(res.stderr, file=sys.stderr)
        return res.returncode
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"[ERRORE] {e}")
        return 1


def backup_news_json() -> None:
    backups_dir = NEWS_DIR / 'backups'
    backups_dir.mkdir(parents=True, exist_ok=True)
    if NEWS_JSON_PATH.exists():
        ts = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
        dest = backups_dir / f'news_{ts}.json'
        shutil.copy2(NEWS_JSON_PATH, dest)
        print(f"Backup creato: {dest}")
    else:
        print("Nessun news.json trovato da salvare.")


def restore_news_json() -> None:
    backups_dir = NEWS_DIR / 'backups'
    files = sorted(backups_dir.glob('*.json'))
    if not files:
        print("Nessun backup disponibile.")
        return
    print("Backup disponibili:")
    for i, f in enumerate(files, start=1):
        print(f"  {i}) {f.name}")
    choice = input("Seleziona numero backup da ripristinare: ").strip()
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(files):
            print("Scelta non valida.")
            return
    except Exception:
        print("Scelta non valida.")
        return
    src = files[idx]
    shutil.copy2(src, NEWS_JSON_PATH)
    print(f"Ripristinato: {src.name} -> {NEWS_JSON_PATH}")


def open_news_index() -> None:
    index_path = PAGES_DIR / 'news.html'
    if not index_path.exists():
        print("pages/news.html non esiste ancora. Genera prima le pagine.")
        return
    webbrowser.open(index_path.resolve().as_uri())
    print("Aperta pagina News nel browser.")


def menu_loop() -> None:
    while True:
        print("\n=== ARCS-VV – Gestione Sito/Blog ===")
        print("1) Normalizza news.json (pulisce date/titoli/estratti, fa backup)")
        print("2) Genera sito principale (templates -> pages)")
        print("3) Genera pagine News (indice + dettagli) senza aggiunte")
        print("4) Aggiungi NUOVA News (procedura interattiva in console)")
        print("5) Avvia Blog Manager (GUI – Windows)")
        print("6) Crea backup manuale di news.json")
        print("7) Ripristina backup di news.json")
        print("8) Apri pagina News nel browser")
        print("9) Esci")
        choice = input("Seleziona un'opzione: ").strip()

        if choice == '1':
            run_script(Path('pages/news/dev/normalize_news_json.py'))
        elif choice == '2':
            run_script(Path('dev/genera_sito.py'))
        elif choice == '3':
            # Risponde 'n' alla domanda di aggiunta nuova news
            run_script(Path('pages/news/dev/genera_news.py'), input_text='n\n')
        elif choice == '4':
            # Apre generatore News interattivo attaccato alla console
            run_script(Path('pages/news/dev/genera_news.py'), attach=True)
        elif choice == '5':
            print("Avvio Blog Manager... (richiede Tkinter su Windows)")
            run_script(Path('pages/news/dev/arcs_blog_manager.py'), attach=True)
        elif choice == '6':
            backup_news_json()
        elif choice == '7':
            restore_news_json()
        elif choice == '8':
            open_news_index()
        elif choice == '9':
            print("Uscita.")
            break
        else:
            print("Scelta non valida.")


if __name__ == '__main__':
    menu_loop()
import json
from pathlib import Path
import re

NEWS_DIR = Path("..", "news")
NEWS_JSON = NEWS_DIR / "news.json"

def estrai_titolo(html_path):
    try:
        with open(html_path, encoding="utf-8") as f:
            content = f.read()
        m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        m = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return html_path.stem

def main():
    # Carica news.json esistente
    if NEWS_JSON.exists():
        with open(NEWS_JSON, encoding="utf-8") as f:
            news = json.load(f)
    else:
        news = []

    # Slug già presenti
    slug_set = {item["slug"] for item in news if "slug" in item}

    # Scansiona tutti gli HTML
    nuovi = 0
    for html_file in NEWS_DIR.glob("*.html"):
        slug = html_file.stem
        if slug not in slug_set:
            titolo = estrai_titolo(html_file)
            news.append({
                "title": titolo,
                "slug": slug,
                "author": "ARCS-VV",
                "date": "",
            })
            print(f"Aggiunto: {slug} ({titolo})")
            nuovi += 1

    # Salva solo se ci sono novità
    if nuovi:
        with open(NEWS_JSON, "w", encoding="utf-8") as f:
            json.dump(news, f, ensure_ascii=False, indent=2)
        print(f"✅ news.json aggiornato con {nuovi} nuove news.")
    else:
        print("Nessuna news da aggiungere: news.json già allineato.")

if __name__ == "__main__":
    main()
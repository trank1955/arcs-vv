#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

SRC_JSON = ROOT / 'pages' / 'news' / 'news.json'
DST_DIR = ROOT / 'public' / 'pages' / 'news'
DST_JSON = DST_DIR / 'news.json'

SRC_POSTS_DIR = ROOT / 'pages' / 'news'

def copy_news_json():
    DST_DIR.mkdir(parents=True, exist_ok=True)
    if not SRC_JSON.exists():
        print(f"[warn] Sorgente news.json non trovato: {SRC_JSON}")
        return False
    shutil.copy(SRC_JSON, DST_JSON)
    print(f"[ok] Copiato JSON: {SRC_JSON} -> {DST_JSON}")
    return True

def copy_post_htmls():
    if not SRC_POSTS_DIR.exists():
        print(f"[warn] Cartella sorgente post non trovata: {SRC_POSTS_DIR}")
        return 0
    count = 0
    for html in SRC_POSTS_DIR.glob('*.html'):
        # Evita di sovrascrivere la lista e la pagina dinamica nel public
        if html.stem in { 'news', 'news_post' }:
            continue
        dst = DST_DIR / html.name
        shutil.copy(html, dst)
        count += 1
    print(f"[ok] Copiati {count} post HTML in {DST_DIR}")
    return count

def main():
    json_ok = copy_news_json()
    posts_n = copy_post_htmls()
    if not json_ok and posts_n == 0:
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())


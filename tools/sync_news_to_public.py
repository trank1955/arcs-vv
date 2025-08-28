#!/usr/bin/env python3
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'pages' / 'news' / 'news.json'
DST_DIR = ROOT / 'public' / 'pages' / 'news'
DST = DST_DIR / 'news.json'

def main():
    if not SRC.exists():
        print(f' sorgente non trovato: {SRC}')
        return 1
    DST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(SRC, DST)
    print(f' Copiato: {SRC} -> {DST}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())


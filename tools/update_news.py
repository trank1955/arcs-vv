#!/usr/bin/env python3
from __future__ import annotations
"""
Script unico per aggiornare le news:
1) Rigenera pages/news/news.json a partire dagli HTML in pages/news/
2) Copia news.json e i post HTML aggiornati in public/pages/news/

Uso: python3 tools/update_news.py
"""

def main() -> int:
    # Assicura import dei moduli del progetto quando eseguito da tools/
    import sys
    from pathlib import Path
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    # 1) Rigenera news.json dagli HTML
    try:
        from tools.blog_manager.blog_manager import generate_news_json_from_html, NEWS_JSON_PATH  # type: ignore
    except Exception as e:
        print(f"[errore] impossibile importare generate_news_json_from_html: {e}")
        return 1
    n = generate_news_json_from_html()
    print(f"[gen] Rigenerato news.json con {n} post → {NEWS_JSON_PATH}")

    # 2) Deploy su public/
    try:
        from tools.deploy_news import main as deploy_news_main  # type: ignore
    except Exception as e:
        print(f"[errore] impossibile importare deploy_news: {e}")
        return 1
    rc = deploy_news_main()
    if rc == 0:
        print("[ok] Deploy news completato")
    else:
        print(f"[warn] Deploy news ha restituito codice {rc}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())

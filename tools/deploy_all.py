#!/usr/bin/env python3
from __future__ import annotations
import shutil
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'

PAGES_SRC = ROOT / 'pages'
PAGES_DST = PUBLIC / 'pages'

ICONS_SRC = ROOT / 'icons'
ICONS_DST = PUBLIC / 'icons'

IMMAGINI_SRC = ROOT / 'immagini'
IMMAGINI_DST = PUBLIC / 'immagini'
PDF_SRC = ROOT / 'pdf'
PDF_DST = PUBLIC / 'pdf'

def copy_file(src: Path, dst: Path) -> bool:
    if not src.exists():
        print(f"[skip] manca sorgente: {src}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"[ok]  file  {src} -> {dst}")
    return True

def copy_tree(src: Path, dst: Path, include_exts: set[str] | None = None) -> int:
    if not src.exists():
        print(f"[skip] cartella non trovata: {src}")
        return 0
    count = 0
    for path in src.rglob('*'):
        if path.is_dir():
            continue
        if include_exts and path.suffix.lower() not in include_exts:
            continue
        rel = path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        count += 1
    print(f"[ok]  copiati {count} file da {src} a {dst}")
    return count

def deploy_news() -> None:
    try:
        from tools.deploy_news import main as deploy_news_main  # type: ignore
    except Exception:
        # Fallback: simple copy of news.json
        SRC_JSON = PAGES_SRC / 'news' / 'news.json'
        DST_JSON = PAGES_DST / 'news' / 'news.json'
        if SRC_JSON.exists():
            DST_JSON.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SRC_JSON, DST_JSON)
            print(f"[ok] news.json copiato (fallback): {SRC_JSON} -> {DST_JSON}")
        else:
            print("[warn] news.json non trovato, salta")
        return
    rc = deploy_news_main()
    if rc == 0:
        print("[ok] deploy_news completato")
    else:
        print(f"[warn] deploy_news ha restituito codice {rc}")

def zip_public() -> Path:
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_base = ROOT / f'public_dist_{ts}'
    zip_path = shutil.make_archive(str(archive_base), 'zip', root_dir=PUBLIC)
    print(f"[ok] archivio creato: {zip_path}")
    return Path(zip_path)

def main() -> int:
    # 1) Assicurati che la struttura base esista
    PAGES_DST.mkdir(parents=True, exist_ok=True)

    # 2) Sincronizza file dinamici e news
    copy_file(ROOT / 'menu.js', PUBLIC / 'menu.js')
    copy_file(ROOT / 'main.css', PUBLIC / 'main.css')
    copy_file(PAGES_SRC / 'news.html', PAGES_DST / 'news.html')
    copy_file(PAGES_SRC / 'news_post.html', PAGES_DST / 'news_post.html')
    deploy_news()

    # 3) Risorse statiche
    copy_tree(ICONS_SRC, ICONS_DST)
    copy_tree(IMMAGINI_SRC, IMMAGINI_DST)
    copy_tree(PDF_SRC, PDF_DST, include_exts={'.pdf', '.PDF'})

    # 4) Crea pacchetto zip pronto da caricare
    zip_public()
    print("[done] Deploy all completato.")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

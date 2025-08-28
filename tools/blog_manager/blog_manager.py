#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.ttk import Notebook
import os
from datetime import datetime
from pathlib import Path
import webbrowser
import json
import re
import html
import shutil
import platform
import subprocess
import sys

# === Logging incrementale su file ===
def log_to_file(message):
    log_path = Path(__file__).parent / "log_blog_manager.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# === Funzioni locali per gestione post ===
def _detect_dirs():
    """Rende robusti i percorsi cercando la root del progetto che contiene 'pages/news'."""
    here = Path(__file__).resolve().parent
    candidates = [here] + list(here.parents)
    project_root = None
    for cand in candidates:
        if (cand / "pages" / "news").exists():
            project_root = cand
            break
    # Fallback: mantieni la cartella 2 livelli sopra
    if project_root is None:
        project_root = here.parent.parent
    pages_dir = project_root / "pages"
    news_dir = pages_dir / "news"
    immagini_dir = project_root / "immagini"
    pdf_dir = project_root / "pdf"
    backups_dir = news_dir / "backups"
    return project_root, pages_dir, news_dir, immagini_dir, pdf_dir, backups_dir

PROJECT_ROOT, PAGES_DIR, NEWS_HTML_DIR, IMMAGINI_DIR, PDF_DIR, BACKUP_DIR = _detect_dirs()
NEWS_JSON_PATH = NEWS_HTML_DIR / "news.json"

def create_backup():
    """Crea un backup di news.json"""
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"news_{timestamp}.json"
    if NEWS_JSON_PATH.exists():
        shutil.copy(NEWS_JSON_PATH, backup_path)
        log_to_file(f"Backup creato: {backup_path}")

def load_posts():
    if NEWS_JSON_PATH.exists():
        with open(NEWS_JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    create_backup()  # Crea backup prima di salvare
    with open(NEWS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def delete_post_by_slug(slug):
    posts = load_posts()
    posts = [p for p in posts if p["slug"] != slug]
    save_posts(posts)
    html_path = NEWS_HTML_DIR / f"{slug}.html"
    if html_path.exists():
        try:
            html_path.unlink()
            log_to_file(f"File HTML eliminato: {html_path}")
        except Exception as e:
            log_to_file(f"Errore eliminazione HTML: {e}")
            return False
    return True

def get_post_by_slug(slug):
    posts = load_posts()
    for p in posts:
        if p["slug"] == slug:
            return p
    return None

def update_post(slug, new_data):
    # Sanitizza gli input per prevenire problemi HTML/XSS
    sanitized_data = {}
    for key, value in new_data.items():
        if isinstance(value, str):
            # Conserva i tag HTML solo nel campo content
            if key == "content":
                sanitized_data[key] = value.strip()
            else:
                sanitized_data[key] = html.escape(value.strip())
        else:
            sanitized_data[key] = value
    
    posts = load_posts()
    for i, p in enumerate(posts):
        if p["slug"] == slug:
            posts[i].update(sanitized_data)
            break
    save_posts(posts)
    return True

def generate_news_json_from_html():
    """Genera news.json a partire dai file HTML trovati in pages/news, estraendo tutti i dati possibili."""
    html_dir = NEWS_HTML_DIR
    news = []
    for html_file in html_dir.glob("*.html"):
        try:
            with open(html_file, encoding="utf-8") as f:
                content = f.read()
            # Estrai titolo
            title = None
            m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if m:
                title = m.group(1).strip()
            else:
                m = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE)
                if m:
                    title = m.group(1).strip()
            # Estrai data
            date = None
            m = re.search(r'<meta[^>]*name=["\"]?date["\"]?[^>]*content=["\"]?([\d\-/]+)["\"]?', content, re.IGNORECASE)
            if m:
                date = m.group(1)
            # Estrai autore
            author = None
            m = re.search(r'<meta[^>]*name=["\"]?author["\"]?[^>]*content=["\"]?([^"\">]+)["\"]?', content, re.IGNORECASE)
            if m:
                author = m.group(1).strip()
            # Estrai immagine (prima <img ... src=...>)
            image = None
            m = re.search(r'<img[^>]*src=["\']([^"\'>]+)["\']', content, re.IGNORECASE)
            if m:
                image = m.group(1).strip()
            # Estrai riassunto (prima <p>...</p> dopo <h3>Riassunto</h3> oppure primo <p>)
            excerpt = None
            m = re.search(r'<h3>\s*Riassunto\s*</h3>\s*<p>(.*?)</p>', content, re.IGNORECASE|re.DOTALL)
            if m:
                excerpt = m.group(1).strip()
            else:
                m = re.search(r'<p>(.*?)</p>', content, re.IGNORECASE|re.DOTALL)
                if m:
                    excerpt = m.group(1).strip()
            
            # Estrai contenuto (dopo il tag <hr>)
            full_content = None
            hr_match = re.search(r'<hr[^>]*>', content, re.IGNORECASE)
            if hr_match:
                hr_end = hr_match.end()
                body_close = content.find('</body>', hr_end)
                if body_close != -1:
                    full_content = content[hr_end:body_close].strip()
            else:
                # Fallback: estrai tutto il body
                m = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE|re.DOTALL)
                if m:
                    full_content = m.group(1).strip()
            
            slug = html_file.stem
            post = {
                "title": title or slug,
                "slug": slug,
                "date": date or "",
                "author": author or "ARCS-VV"
            }
            if image:
                post["image"] = image
            if excerpt:
                post["excerpt"] = excerpt
            if full_content:
                post["content"] = full_content
            news.append(post)
        except Exception as e:
            log_to_file(f"Errore lettura {html_file}: {e}")
    save_posts(news)
    log_to_file(f"news.json rigenerato con {len(news)} post trovati in HTML.")
    return len(news)

def render_article_html(data: dict) -> str:
    """Rende un HTML di articolo con meta, menu e struttura coerente con il sito."""
    title = html.escape(data.get('title',''))
    date = html.escape(data.get('date',''))
    author = html.escape(data.get('author','ARCS-VV'))
    image = html.escape(data.get('image',''))
    pdf = html.escape(data.get('pdf',''))
    video = data.get('video','').strip()
    excerpt = html.escape(data.get('excerpt',''))
    content = data.get('content','')
    def _rel_asset(src: str) -> str:
        if not src:
            return ''
        # Normalizza i percorsi per l'HTML sotto pages/news/*.html
        if src.startswith('../'):
            return src
        if src.startswith('immagini/'):
            return '../' + src
        if src.startswith('pdf/'):
            return '../' + src
        # Se solo nome file immagine
        if any(src.lower().endswith(ext) for ext in ('.jpg','.jpeg','.png','.gif','.webp','.svg')):
            return '../immagini/' + src
        if src.lower().endswith('.pdf'):
            return '../pdf/' + src
        return src

    img_src = _rel_asset(image)
    img_tag = f"\n    <img src=\"{img_src}\" alt=\"Immagine articolo\" style=\"max-width:100%;height:auto;border-radius:8px;margin:1em 0;\">" if image else ""

    pdf_link = ''
    if pdf:
        pdf_href = _rel_asset(pdf)
        pdf_link = f"\n    <p style=\"margin:1em 0;\"><a href=\"{pdf_href}\" target=\"_blank\" rel=\"noopener\" style=\"font-weight:600;color:#006699;\">📄 Scarica PDF</a></p>"

    def _embed_video(url: str) -> str:
        u = url.strip()
        if not u:
            return ''
        # YouTube
        # Supporta formati: https://youtu.be/ID, https://www.youtube.com/watch?v=ID
        import re
        yt_id = None
        m = re.search(r'youtu\.be/([A-Za-z0-9_-]{6,})', u)
        if not m:
            m = re.search(r'v=([A-Za-z0-9_-]{6,})', u)
        if m:
            yt_id = m.group(1)
        if yt_id:
            return f"\n    <div style=\"position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;margin:1em 0;\"><iframe src=\"https://www.youtube.com/embed/{yt_id}\" frameborder=\"0\" allowfullscreen style=\"position:absolute;top:0;left:0;width:100%;height:100%;\"></iframe></div>"
        # Vimeo
        m = re.search(r'vimeo\.com/(?:video/)?(\d+)', u)
        if m:
            vid = m.group(1)
            return f"\n    <div style=\"position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;margin:1em 0;\"><iframe src=\"https://player.vimeo.com/video/{vid}\" frameborder=\"0\" allowfullscreen style=\"position:absolute;top:0;left:0;width:100%;height:100%;\"></iframe></div>"
        # Link semplice se non riconosciuto
        return f"\n    <p style=\"margin:1em 0;\"><a href=\"{html.escape(u)}\" target=\"_blank\" rel=\"noopener\">🎬 Guarda il video</a></p>"

    video_block = _embed_video(video) if video else ''
    return f"""<!DOCTYPE html>
<html lang='it'>
<head>
  <meta charset='UTF-8'>
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{title}</title>
  <meta name=\"date\" content=\"{date}\">
  <meta name=\"author\" content=\"{author}\">
  <link rel=\"icon\" type=\"image/x-icon\" href=\"../icons/favicon.ico\">
  <link rel=\"stylesheet\" href=\"../main.css\"> 
</head>
<body class=\"page-news\">
  <div id=\"menu-inject\"></div>
  <script src=\"../menu.js\"></script>
  <main style=\"max-width:800px;margin:auto;padding:1em;\"> 
    <h1>{title}</h1>
    <p style=\"color:#888;font-size:0.95em;\">Pubblicato il {date} da {author}</p>
    {img_tag}
    <h3>Riassunto</h3>
    <p>{excerpt}</p>
    {pdf_link}
    {video_block}
    <hr>
    <div class=\"blog-content\">
      {content}
    </div>
    <p style=\"margin-top:2em;\"><a href=\"../news.html\">&larr; Torna all'elenco news</a></p>
  </main>
</body>
</html>"""

def _deploy_news_quick(saved_slug: str | None = None, data: dict | None = None) -> dict:
    """Copia news.json e i file del post salvato in public/ e restituisce un report.
    Tenta prima tools.deploy_news, poi sincronizza JSON/HTML e asset (immagine/pdf).
    """
    report = {
        'used_standard': False,
        'json': None,
        'html': None,
        'image': None,
        'pdf': None,
        'errors': []
    }
    # 1) Prova deploy standard
    try:
        from tools.deploy_news import main as deploy_news_main  # type: ignore
        rc = deploy_news_main()
        report['used_standard'] = True
        log_to_file(f"deploy_news.py eseguito con codice {rc}")
    except Exception as e:
        msg = f"deploy_news import fallito, uso fallback: {e}"
        report['errors'].append(msg)
        log_to_file(msg)

    # 2) Copia mirata (fallback e/o asset extra)
    try:
        public_root = PROJECT_ROOT / 'public'
        public_news_dir = public_root / 'pages' / 'news'
        public_news_dir.mkdir(parents=True, exist_ok=True)
        # JSON sempre aggiornato
        if NEWS_JSON_PATH.exists():
            dst_json = public_news_dir / 'news.json'
            shutil.copy2(NEWS_JSON_PATH, dst_json)
            report['json'] = str(dst_json)
        # HTML del post salvato
        if saved_slug:
            src_html = NEWS_HTML_DIR / f"{saved_slug}.html"
            if src_html.exists():
                dst_html = public_news_dir / src_html.name
                shutil.copy2(src_html, dst_html)
                report['html'] = str(dst_html)
        # Sincronizza asset fondamentali (immagine/pdf) del post appena salvato
        if data:
            img = str(data.get('image','')).strip()
            pdf = str(data.get('pdf','')).strip()
            # Copia immagine
            if img:
                src_img_path = Path(img)
                if not src_img_path.is_absolute():
                    if img.startswith('immagini/'):
                        src_img_path = PROJECT_ROOT / img
                    else:
                        src_img_path = IMMAGINI_DIR / img
                if src_img_path.exists():
                    dst_img_dir = public_root / 'immagini'
                    dst_img_dir.mkdir(parents=True, exist_ok=True)
                    dst_img = dst_img_dir / src_img_path.name
                    shutil.copy2(src_img_path, dst_img)
                    report['image'] = str(dst_img)
            # Copia PDF
            if pdf:
                src_pdf_path = Path(pdf)
                if not src_pdf_path.is_absolute():
                    if pdf.startswith('pdf/'):
                        src_pdf_path = PROJECT_ROOT / pdf
                    else:
                        src_pdf_path = PDF_DIR / pdf
                if src_pdf_path.exists():
                    dst_pdf_dir = public_root / 'pdf'
                    dst_pdf_dir.mkdir(parents=True, exist_ok=True)
                    dst_pdf = dst_pdf_dir / src_pdf_path.name
                    shutil.copy2(src_pdf_path, dst_pdf)
                    report['pdf'] = str(dst_pdf)
        log_to_file(("Deploy standard + sync asset completato" if report['used_standard'] else "Deploy rapido news completato (fallback)"))
    except Exception as e:
        msg = f"Errore deploy rapido/sync asset: {e}"
        report['errors'].append(msg)
        log_to_file(msg)
    return report

def _open_folder(path: Path):
    try:
        if platform.system() == 'Windows':
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', str(path)])
        else:
            subprocess.Popen(['xdg-open', str(path)])
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile aprire la cartella:\n{path}\n\n{e}")

# === Finestra di dialogo per modifica post ===
class EditPostDialog(tk.Toplevel):
    def __init__(self, parent, post):
        super().__init__(parent.root)
        self.parent = parent
        self.post = post
        self.title(f"Modifica post: {post.get('title','')}")
        self.geometry("800x700")  # Finestra più grande
        self.resizable(True, True)  # Ora è ridimensionabile

        # Variabili
        self.var_title = tk.StringVar(value=post.get('title',''))
        self.var_date = tk.StringVar(value=post.get('date',''))
        self.var_image = tk.StringVar(value=post.get('image',''))
        self.var_pdf = tk.StringVar(value=post.get('pdf',''))
        self.var_video = tk.StringVar(value=post.get('video',''))
        self.var_summary = tk.StringVar(value=post.get('excerpt',''))

        # Layout principale con panedwindow per divisione
        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame sinistro per i metadati
        left_frame = ttk.Frame(main_pane)
        main_pane.add(left_frame, weight=1)

        # Titolo
        ttk.Label(left_frame, text="Titolo:").pack(anchor='w', pady=(0, 5))
        self.entry_title = ttk.Entry(left_frame, textvariable=self.var_title, font=('Arial', 11))
        self.entry_title.pack(fill='x', pady=(0, 10))
        self.entry_title.focus()

        # Data
        ttk.Label(left_frame, text="Data (YYYY-MM-DD):").pack(anchor='w', pady=(0, 5))
        self.entry_date = ttk.Entry(left_frame, textvariable=self.var_date)
        self.entry_date.pack(fill='x', pady=(0, 10))

        # Immagine
        ttk.Label(left_frame, text="Immagine (percorso relativo):").pack(anchor='w', pady=(0, 5))
        img_frame = ttk.Frame(left_frame)
        img_frame.pack(fill='x', pady=(0, 10))
        self.entry_image = ttk.Entry(img_frame, textvariable=self.var_image)
        self.entry_image.pack(side=tk.LEFT, fill='x', expand=True)
        ttk.Button(img_frame, text="Sfoglia", width=8, command=self.browse_image).pack(side=tk.RIGHT, padx=(5, 0))

        # PDF
        ttk.Label(left_frame, text="PDF (percorso relativo):").pack(anchor='w', pady=(10, 5))
        pdf_frame = ttk.Frame(left_frame)
        pdf_frame.pack(fill='x', pady=(0, 10))
        self.entry_pdf = ttk.Entry(pdf_frame, textvariable=self.var_pdf)
        self.entry_pdf.pack(side=tk.LEFT, fill='x', expand=True)
        ttk.Button(pdf_frame, text="Sfoglia", width=8, command=self.browse_pdf).pack(side=tk.RIGHT, padx=(5, 0))

        # Video URL
        ttk.Label(left_frame, text="Video (URL YouTube o Vimeo):").pack(anchor='w', pady=(10, 5))
        self.entry_video = ttk.Entry(left_frame, textvariable=self.var_video)
        self.entry_video.pack(fill='x', pady=(0, 10))

        # Riassunto
        ttk.Label(left_frame, text="Riassunto:").pack(anchor='w', pady=(0, 5))
        self.entry_summary = scrolledtext.ScrolledText(left_frame, height=4, font=('Arial', 10))
        self.entry_summary.pack(fill='x', pady=(0, 10))
        self.entry_summary.insert('1.0', post.get('excerpt',''))

        # Frame destro per il contenuto
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=2)

        # Contenuto
        ttk.Label(right_frame, text="Contenuto HTML:").pack(anchor='w', pady=(0, 5))
        self.text_content = scrolledtext.ScrolledText(right_frame, font=('Arial', 10))
        self.text_content.pack(fill='both', expand=True)
        self.text_content.insert('1.0', post.get('content',''))

        # Pulsanti
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text="Anteprima", command=self.preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Salva", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Annulla", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def _lift_for_dialog(self):
        try:
            self.lift()
            self.attributes('-topmost', True)
            self.update()
        except Exception:
            pass

    def _lower_after_dialog(self):
        try:
            self.attributes('-topmost', False)
        except Exception:
            pass

    def browse_image(self):
        initial_dir = IMMAGINI_DIR.resolve()
        self._lift_for_dialog()
        file_path = filedialog.askopenfilename(
            parent=self,
            initialdir=str(initial_dir),
            title="Seleziona immagine",
            filetypes=(("Immagini", ("*.jpg","*.jpeg","*.png","*.gif","*.webp","*.JPG","*.JPEG","*.PNG","*.GIF","*.WEBP")), ("Tutti i file", "*.*"))
        )
        self._lower_after_dialog()
        if file_path:
            # Crea percorso relativo rispetto alla root del progetto
            try:
                rel_path = Path(file_path).resolve().relative_to(PROJECT_ROOT.resolve())
            except Exception:
                rel_path = Path(file_path)
            self.var_image.set(str(rel_path))

    def browse_pdf(self):
        initial_dir = PDF_DIR.resolve()
        self._lift_for_dialog()
        file_path = filedialog.askopenfilename(
            parent=self,
            initialdir=str(initial_dir),
            title="Seleziona PDF",
            filetypes=(("PDF", ("*.pdf","*.PDF")), ("Tutti i file", "*.*"))
        )
        self._lower_after_dialog()
        if file_path:
            try:
                rel_path = Path(file_path).resolve().relative_to(PROJECT_ROOT.resolve())
            except Exception:
                rel_path = Path(file_path)
            self.var_pdf.set(str(rel_path))

    def preview(self):
        """Mostra anteprima HTML in browser"""
        # Salva l'anteprima dentro pages/news per avere percorsi relativi corretti (../immagini, ../pdf)
        temp_path = NEWS_HTML_DIR / "temp_preview.html"
        try:
            html_content = render_article_html(self._get_form_data())
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            webbrowser.open(f"file://{temp_path.resolve()}")
        except Exception as e:
            messagebox.showerror("Errore anteprima", f"Impossibile generare anteprima:\n{e}")

    def _get_form_data(self):
        return {
            'title': self.var_title.get().strip(),
            'date': self.var_date.get().strip(),
            'image': self.var_image.get().strip(),
            'pdf': self.var_pdf.get().strip(),
            'video': self.var_video.get().strip(),
            'excerpt': self.entry_summary.get('1.0', 'end').strip(),
            'content': self.text_content.get('1.0', 'end').strip(),
        }

    def save(self):
        data = self._get_form_data()
        slug = self.post.get('slug')
        
        # Verifica esistenza immagine (supporta path relativi/assoluti)
        img_path = (IMMAGINI_DIR / data['image']).resolve() if not str(data['image']).startswith(str(IMMAGINI_DIR)) else Path(data['image']).resolve()
        if data['image'] and not img_path.exists():
            if not messagebox.askyesno(
                "Immagine mancante",
                f"File immagine non trovato:\n{img_path}\n\nVuoi continuare comunque?"
            ):
                return

        # Verifica PDF
        if data.get('pdf'):
            pdf_path = (PDF_DIR / data['pdf']).resolve() if not str(data['pdf']).startswith(str(PDF_DIR)) else Path(data['pdf']).resolve()
            if not pdf_path.exists():
                if not messagebox.askyesno(
                    "PDF mancante",
                    f"File PDF non trovato:\n{pdf_path}\n\nVuoi continuare comunque?"
                ):
                    return
        
        # Aggiorna dati post
        update_post(slug, data)
        
        # Aggiorna file HTML
        html_path = NEWS_HTML_DIR / f"{slug}.html"
        try:
            with open(html_path, "w", encoding="utf-8") as f:
                html_content = render_article_html(data)
                f.write(html_content)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore aggiornamento file HTML:\n{e}")
            return
        
        self.parent.refresh_posts_list()
        # Deploy automatico su public/
        details = None
        try:
            report = _deploy_news_quick(saved_slug=slug, data=data)
            lines = []
            lines.append(f"Metodo: {'deploy_news.py' if report.get('used_standard') else 'copia rapida'}")
            lines.append(f"JSON: {'ok → ' + report['json'] if report.get('json') else 'saltato'}")
            lines.append(f"HTML: {'ok → ' + report['html'] if report.get('html') else 'saltato'}")
            lines.append(f"Immagine: {'ok → ' + report['image'] if report.get('image') else ('assente' if not data.get('image') else 'non copiata')} ")
            lines.append(f"PDF: {'ok → ' + report['pdf'] if report.get('pdf') else ('assente' if not data.get('pdf') else 'non copiato')}")
            if report.get('errors'):
                lines.append("Note: " + " | ".join(report['errors']))
            details = "\n".join(lines)
        except Exception as _e:
            log_to_file(f"Deploy automatico fallito: {_e}")
        msg = "Post modificato e pubblicato in public/!"
        if details:
            msg += "\n\n" + details
        try:
            self.show_publish_report(msg)
        finally:
            self.destroy()

    def show_publish_report(self, message: str):
        top = tk.Toplevel(self.parent.root)
        top.title("Pubblicazione completata")
        top.geometry("720x420")
        top.resizable(True, True)
        try:
            top.transient(self.parent.root)
            top.grab_set()
        except Exception:
            pass

        lbl = ttk.Label(top, text="Dettagli pubblicazione:", font=('Arial', 11, 'bold'))
        lbl.pack(anchor='w', padx=12, pady=(12, 6))

        text = scrolledtext.ScrolledText(top, height=16, font=('Consolas', 10))
        text.pack(fill='both', expand=True, padx=12, pady=(0, 12))
        text.insert('1.0', message)
        text.configure(state='disabled')

        btns = ttk.Frame(top)
        btns.pack(fill='x', padx=12, pady=(0, 12))

        def open_public_news():
            target = PROJECT_ROOT / 'public' / 'pages' / 'news'
            _open_folder(target)

        ttk.Button(btns, text="Apri cartella public/news", command=open_public_news).pack(side=tk.LEFT)
        ttk.Button(btns, text="Chiudi", command=top.destroy).pack(side=tk.RIGHT)

    def _render_html(self, data):
        # Template HTML con escaping dei campi testuali
        return f"""<!DOCTYPE html>
<html lang='it'>
<head>
    <meta charset='UTF-8'>
    <title>{html.escape(data['title'])}</title>
    <meta name="date" content="{html.escape(data['date'])}">
    <meta name="author" content="ARCS-VV">
</head>
<body>
    <h1>{html.escape(data['title'])}</h1>
    <p><em>{html.escape(data['date'])}</em></p>
    <img src="../immagini/{html.escape(data['image'])}" alt="Immagine" style="max-width:100%;height:auto;">
    <h3>Riassunto</h3>
    <p>{html.escape(data['excerpt'])}</p>
    <hr>
    <div>{data['content']}</div>
</body>
</html>"""

# === MAIN APP ===
class BlogManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ARCS-VV Blog Manager")
        try:
            self.root.state('zoomed')  # Windows
        except Exception:
            self.root.attributes('-zoomed', True)  # Alcuni ambienti Linux

        # Tabs
        self.notebook = Notebook(self.root)
        self.tab_posts = ttk.Frame(self.notebook)
        self.tab_log = ttk.Frame(self.notebook)
        self.tab_backups = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_posts, text="Gestione News")
        self.notebook.add(self.tab_log, text="Log")
        self.notebook.add(self.tab_backups, text="Backup")
        self.notebook.pack(fill='both', expand=True)

        # Layout verticale: lista post sopra, bottoni sotto
        self.tab_posts.rowconfigure(0, weight=1)
        self.tab_posts.rowconfigure(1, weight=0)
        self.tab_posts.columnconfigure(0, weight=1)

        # Lista post
        tree_frame = ttk.Frame(self.tab_posts)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,0))
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.posts_tree = ttk.Treeview(
            tree_frame, 
            columns=("slug", "title", "date", "file"), 
            show="headings",
            yscrollcommand=tree_scroll.set
        )
        tree_scroll.config(command=self.posts_tree.yview)
        self.posts_tree.heading("slug", text="Slug")
        self.posts_tree.heading("title", text="Titolo")
        self.posts_tree.heading("date", text="Data")
        self.posts_tree.heading("file", text="File HTML")
        self.posts_tree.column("slug", width=150)
        self.posts_tree.column("title", width=250)
        self.posts_tree.column("date", width=100)
        self.posts_tree.column("file", width=150)
        self.posts_tree.pack(fill='both', expand=True)
        self.posts_tree.bind("<Double-1>", self.on_double_click)

        # Pulsanti azione in basso
        btn_frame = ttk.Frame(self.tab_posts)
        btn_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))
        ttk.Button(btn_frame, text="Nuovo", command=self.create_new_post).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Nuovo da template", command=self.create_new_post_from_template).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Modifica", command=self.edit_selected_post).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Elimina", command=self.delete_selected_post).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Apri HTML", command=self.open_html_selected_post).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_posts_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Rigenera news.json", command=self.generate_news_json_from_html).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Apri cartella Public/News", command=lambda: _open_folder(PROJECT_ROOT / 'public' / 'pages' / 'news')).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Apri cartella News", command=lambda: _open_folder(NEWS_HTML_DIR)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Apri cartella PDF", command=lambda: _open_folder(PDF_DIR)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Apri cartella Immagini", command=lambda: _open_folder(IMMAGINI_DIR)).pack(side=tk.RIGHT, padx=5)

        # Log
        self.log_text = scrolledtext.ScrolledText(
            self.tab_log, 
            state='disabled', 
            height=20,
            font=('Consolas', 10)
        )
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)

        # Backup manager
        backup_frame = ttk.Frame(self.tab_backups)
        backup_frame.pack(fill='both', expand=True, padx=10, pady=10)
        ttk.Label(backup_frame, text="Backup disponibili:").pack(anchor='w')
        self.backup_listbox = tk.Listbox(
            backup_frame,
            height=10,
            selectmode=tk.SINGLE
        )
        self.backup_listbox.pack(fill='both', expand=True, pady=5)
        btn_frame_backup = ttk.Frame(backup_frame)
        btn_frame_backup.pack(fill='x', pady=5)
        ttk.Button(btn_frame_backup, text="Ricarica", command=self.load_backups).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_backup, text="Ripristina", command=self.restore_backup).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_backup, text="Elimina", command=self.delete_backup).pack(side=tk.RIGHT, padx=5)

        self.load_backups()
        self.refresh_posts_list()

    def on_double_click(self, event):
        self.edit_selected_post()

    def load_backups(self):
        """Carica l'elenco dei backup"""
        self.backup_listbox.delete(0, tk.END)
        if BACKUP_DIR.exists():
            backups = sorted(BACKUP_DIR.glob("*.json"), key=os.path.getmtime, reverse=True)
            for backup in backups:
                self.backup_listbox.insert(tk.END, backup.name)

    def restore_backup(self):
        """Ripristina un backup selezionato"""
        selection = self.backup_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un backup da ripristinare")
            return
            
        backup_name = self.backup_listbox.get(selection[0])
        backup_path = BACKUP_DIR / backup_name
        
        if messagebox.askyesno(
            "Conferma ripristino",
            f"Ripristinare il backup?\n{backup_name}\n\nQuesta operazione sovrascriverà l'attuale news.json"
        ):
            try:
                shutil.copy(backup_path, NEWS_JSON_PATH)
                self.refresh_posts_list()
                messagebox.showinfo("Successo", "Backup ripristinato con successo!")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante il ripristino:\n{e}")

    def delete_backup(self):
        """Elimina un backup selezionato"""
        selection = self.backup_listbox.curselection()
        if not selection:
            return
            
        backup_name = self.backup_listbox.get(selection[0])
        backup_path = BACKUP_DIR / backup_name
        
        if messagebox.askyesno(
            "Conferma eliminazione",
            f"Eliminare il backup?\n{backup_name}"
        ):
            try:
                backup_path.unlink()
                self.load_backups()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'eliminazione:\n{e}")

    def load_log(self):
        log_path = Path(__file__).parent / "log_blog_manager.txt"
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        if log_path.exists():
            with open(log_path, encoding="utf-8") as f:
                self.log_text.insert('1.0', f.read())
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)  # Scorri alla fine

    def refresh_posts_list(self):
        self.posts_tree.delete(*self.posts_tree.get_children())
        posts = load_posts()
        html_files = {f.stem for f in NEWS_HTML_DIR.glob("*.html")}
        
        for post in posts:
            slug = post.get("slug", "")
            title = post.get("title", "")
            date = post.get("date", "")
            file_exists = "OK" if slug in html_files else "MANCANTE"
            self.posts_tree.insert(
                "", 
                "end", 
                values=(slug, title, date, f"{slug}.html"), 
                tags=("missing",) if file_exists=="MANCANTE" else ()
            )
        
        self.posts_tree.tag_configure("missing", background="#ffcccc")
        log_to_file("Lista post aggiornata.")
        self.load_log()

    def get_selected_slug(self):
        sel = self.posts_tree.selection()
        if not sel:
            return None
        return self.posts_tree.item(sel[0], "values")[0]

    def create_new_post(self):
        # Crea un nuovo post con placeholder e salva subito (senza aprire editor)
        slug = datetime.now().strftime("post_%Y%m%d%H%M%S")
        new_post = {
            'title': "Nuovo Post",
            'slug': slug,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'author': "ARCS-VV",
            'image': "",
            'excerpt': "Breve riassunto dell'articolo...",
            'content': "<p>Scrivi qui il contenuto dell'articolo.</p>"
        }
        
        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)
        
        # Crea file HTML con struttura pronta
        html_path = NEWS_HTML_DIR / f"{slug}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(render_article_html(new_post))
        
        self.refresh_posts_list()
        messagebox.showinfo("Successo", f"Nuovo post creato: {slug}")

    def create_new_post_from_template(self):
        # Crea un nuovo post con placeholder e apre direttamente l'editor
        slug = datetime.now().strftime("post_%Y%m%d%H%M%S")
        new_post = {
            'title': "Nuovo Post",
            'slug': slug,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'author': "ARCS-VV",
            'image': "",
            'excerpt': "Breve riassunto dell'articolo...",
            'content': "<p>Scrivi qui il contenuto dell'articolo.</p>"
        }

        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)

        # Crea file HTML iniziale
        html_path = NEWS_HTML_DIR / f"{slug}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(render_article_html(new_post))

        self.refresh_posts_list()
        EditPostDialog(self, new_post)

    def edit_selected_post(self):
        slug = self.get_selected_slug()
        if not slug:
            messagebox.showwarning("Selezione mancante", "Seleziona un post da modificare.")
            return
        post = get_post_by_slug(slug)
        if post:
            EditPostDialog(self, post)

    def delete_selected_post(self):
        slug = self.get_selected_slug()
        if not slug:
            messagebox.showwarning("Selezione mancante", "Seleziona un post da eliminare.")
            return
        if messagebox.askyesno(
            "Conferma eliminazione", 
            f"Eliminare il post '{slug}'?\n\nQuesta azione cancellerà sia il record che il file HTML associato."
        ):
            if delete_post_by_slug(slug):
                log_to_file(f"Post '{slug}' eliminato.")
                self.refresh_posts_list()
            else:
                messagebox.showerror("Errore", "Impossibile eliminare completamente il post")

    def open_html_selected_post(self):
        slug = self.get_selected_slug()
        if not slug:
            messagebox.showwarning("Selezione mancante", "Seleziona un post.")
            return
        html_path = NEWS_HTML_DIR / f"{slug}.html"
        if html_path.exists():
            webbrowser.open(str(html_path.resolve()))
        else:
            messagebox.showerror("File mancante", f"Il file HTML per '{slug}' non esiste.")

    def generate_news_json_from_html(self):
        if messagebox.askyesno(
            "Conferma rigenerazione",
            "Questa operazione sovrascriverà l'attuale news.json con dati estratti dai file HTML.\n\nProcedere?"
        ):
            count = generate_news_json_from_html()
            self.refresh_posts_list()
            messagebox.showinfo("Completato", f"news.json rigenerato con {count} post da HTML.")

def main():
    root = tk.Tk()
    app = BlogManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

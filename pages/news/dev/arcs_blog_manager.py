#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.ttk import Notebook
import os
import sys
from datetime import datetime
from pathlib import Path
import webbrowser
import json

# === Utility ===
NEWS_JSON_PATH = Path("..", "news", "news.json")
NEWS_HTML_DIR = Path("..", "news")

def log_to_file(message):
    log_path = Path(__file__).parent / "log_blog_manager.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def load_posts():
    if NEWS_JSON_PATH.exists():
        with open(NEWS_JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(NEWS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def delete_post_by_slug(slug):
    posts = load_posts()
    posts = [p for p in posts if p["slug"] != slug]
    save_posts(posts)
    html_path = NEWS_HTML_DIR / f"{slug}.html"
    if html_path.exists():
        html_path.unlink()
    return True

def get_post_by_slug(slug):
    posts = load_posts()
    for p in posts:
        if p["slug"] == slug:
            return p
    return None

def update_post(slug, new_data):
    posts = load_posts()
    for i, p in enumerate(posts):
        if p["slug"] == slug:
            posts[i].update(new_data)
            break
    save_posts(posts)
    return True

def generate_news_json_from_html():
    import re
    posts = []
    for html_file in NEWS_HTML_DIR.glob("*.html"):
        try:
            with open(html_file, encoding="utf-8") as f:
                html = f.read()
            title = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE)
            date = re.search(r'<em>(.*?)</em>', html, re.IGNORECASE)
            image = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
            excerpt = re.search(r'<h3>Riassunto</h3>\s*<p>(.*?)</p>', html, re.IGNORECASE|re.DOTALL)
            content = re.split(r'<h3>Riassunto</h3>.*?</p>', html, flags=re.IGNORECASE|re.DOTALL)
            slug = html_file.stem
            post = {
                "slug": slug,
                "title": title.group(1).strip() if title else slug,
                "date": date.group(1).strip() if date else "",
                "image": os.path.basename(image.group(1)) if image else "default.jpg",
                "excerpt": excerpt.group(1).strip() if excerpt else "",
                "content": content[1].strip() if len(content)>1 else ""
            }
            posts.append(post)
        except Exception as e:
            log_to_file(f"Errore parsing {html_file.name}: {e}")
    save_posts(posts)
    log_to_file("news.json rigenerato da HTML.")

# === GUI ===
class EditPostDialog(tk.Toplevel):
    def __init__(self, parent, post):
        super().__init__(parent.root)
        self.parent = parent
        self.post = post
        self.title(f"Modifica post: {post.get('title','')}")
        self.geometry("600x600")
        self.resizable(False, False)

        self.var_title = tk.StringVar(value=post.get('title',''))
        self.var_date = tk.StringVar(value=post.get('date',''))
        self.var_image = tk.StringVar(value=post.get('image',''))
        self.var_summary = tk.StringVar(value=post.get('excerpt',''))

        frm = ttk.Frame(self, padding=20)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text="Titolo:").pack(anchor='w')
        self.entry_title = ttk.Entry(frm, textvariable=self.var_title, font=('Arial', 11))
        self.entry_title.pack(fill='x', pady=5)

        ttk.Label(frm, text="Data:").pack(anchor='w')
        self.entry_date = ttk.Entry(frm, textvariable=self.var_date)
        self.entry_date.pack(fill='x', pady=5)

        ttk.Label(frm, text="Immagine (nome file o percorso):").pack(anchor='w')
        self.entry_image = ttk.Entry(frm, textvariable=self.var_image)
        self.entry_image.pack(fill='x', pady=5)

        ttk.Label(frm, text="Riassunto:").pack(anchor='w')
        self.entry_summary = ttk.Entry(frm, textvariable=self.var_summary)
        self.entry_summary.pack(fill='x', pady=5)

        ttk.Label(frm, text="Contenuto:").pack(anchor='w')
        self.text_content = scrolledtext.ScrolledText(frm, height=10, font=('Arial', 10))
        self.text_content.pack(fill='both', pady=5)
        self.text_content.insert('1.0', post.get('content',''))

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill='x', pady=10)
    ttk.Button(btn_frame, text="Salva", command=self.save).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Annulla", command=self.destroy).pack(side='right', padx=5)

    def save(self):
        new_data = {
            'title': self.var_title.get().strip(),
            'date': self.var_date.get().strip(),
            'image': self.var_image.get().strip(),
            'excerpt': self.var_summary.get().strip(),
            'content': self.text_content.get('1.0', 'end').strip(),
        }
        slug = self.post.get('slug')
        update_post(slug, new_data)
        html_path = Path("..", "news", f"{slug}.html")
        if html_path.exists():
            try:
                with open(html_path, "w", encoding="utf-8") as f:
                    html = self._render_html(new_data)
                    f.write(html)
            except Exception as e:
                messagebox.showerror("Errore", f"Errore aggiornamento file HTML:\n{e}")
        self.parent.refresh_posts_list()
        messagebox.showinfo("Successo", "Post modificato con successo!")
        self.destroy()

    def _render_html(self, data):
        html = (
            "<!DOCTYPE html>\n"
            "<html lang='it'>\n"
            "<head>\n"
            "    <meta charset='UTF-8'>\n"
            f"    <title>{data['title']}</title>\n"
            "</head>\n"
            "<body>\n"
            f"    <h1>{data['title']}</h1>\n"
            f"    <p><em>{data['date']}</em></p>\n"
            f"    <img src='../immagini/{data['image']}' alt='Immagine' style='max-width:100%;height:auto;'>\n"
            "    <h3>Riassunto</h3>\n"
            f"    <p>{data['excerpt']}</p>\n"
            "    <hr>\n"
            f"    <div>{data['content'].replace(chr(10),'<br>')}</div>\n"
            "</body>\n"
            "</html>"
        )
        return html

class BlogManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ARCS-VV Blog Manager")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        self.notebook = Notebook(self.root)
        self.tab_posts = ttk.Frame(self.notebook)
        self.tab_log = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_posts, text="Gestione News")
        self.notebook.add(self.tab_log, text="Log")
        self.notebook.pack(fill='both', expand=True)

        self.posts_tree = ttk.Treeview(self.tab_posts, columns=("slug", "title", "date", "file"), show="headings")
        self.posts_tree.heading("slug", text="Slug")
        self.posts_tree.heading("title", text="Titolo")
        self.posts_tree.heading("date", text="Data")
        self.posts_tree.heading("file", text="File HTML")
        self.posts_tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.tab_posts)
        btn_frame.pack(fill='x', padx=10, pady=5)
        ttk.Button(btn_frame, text="Modifica", command=self.edit_selected_post).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Elimina", command=self.delete_selected_post).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Apri HTML", command=self.open_html_selected_post).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Rigenera news.json da HTML", command=self.generate_news_json_from_html).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_posts_list).pack(side='right', padx=5)

        self.log_text = scrolledtext.ScrolledText(self.tab_log, state='disabled', height=20)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.load_log()

        self.refresh_posts_list()

    def load_log(self):
        log_path = Path(__file__).parent / "log_blog_manager.txt"
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        if log_path.exists():
            with open(log_path, encoding="utf-8") as f:
                self.log_text.insert('1.0', f.read())
        self.log_text.config(state='disabled')

    def refresh_posts_list(self):
        self.posts_tree.delete(*self.posts_tree.get_children())
        posts = load_posts()
        html_files = {f.stem for f in NEWS_HTML_DIR.glob("*.html")}
        for post in posts:
            slug = post.get("slug", "")
            title = post.get("title", "")
            date = post.get("date", "")
            file_exists = "OK" if slug in html_files else "MANCANTE"
            self.posts_tree.insert("", "end", values=(slug, title, date, file_exists), tags=("missing",) if file_exists=="MANCANTE" else ())
        self.posts_tree.tag_configure("missing", background="#ffcccc")
        log_to_file("Lista post aggiornata.")
        self.load_log()

    def get_selected_slug(self):
        sel = self.posts_tree.selection()
        if not sel:
            return None
        return self.posts_tree.item(sel[0], "values")[0]

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
        if messagebox.askyesno("Conferma eliminazione", f"Eliminare il post '{slug}'? Questa azione è irreversibile."):
            delete_post_by_slug(slug)
            log_to_file(f"Post '{slug}' eliminato.")
            self.refresh_posts_list()

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
        generate_news_json_from_html()
        self.refresh_posts_list()
        messagebox.showinfo("Completato", "news.json rigenerato da HTML.")

def main():
    root = tk.Tk()
    app = BlogManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
# --- FINE FILE ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        # Estrae dati da tutti i file HTML e rigenera news.json
        posts = []
        for html_file in NEWS_HTML_DIR.glob("*.html"):
            try:
                with open(html_file, encoding="utf-8") as f:
                    html = f.read()
                # Estrazione semplice via regex/stringhe
                import re
                title = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE)
                date = re.search(r'<em>(.*?)</em>', html, re.IGNORECASE)
                image = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
                excerpt = re.search(r'<h3>Riassunto</h3>\s*<p>(.*?)</p>', html, re.IGNORECASE|re.DOTALL)
                content = re.split(r'<h3>Riassunto</h3>.*?</p>', html, flags=re.IGNORECASE|re.DOTALL)
                slug = html_file.stem
                post = {
                    "slug": slug,
                    "title": title.group(1).strip() if title else slug,
                    "date": date.group(1).strip() if date else "",
                    "image": os.path.basename(image.group(1)) if image else "default.jpg",
                    "excerpt": excerpt.group(1).strip() if excerpt else "",
                    "content": content[1].strip() if len(content)>1 else ""
                }
                posts.append(post)
            except Exception as e:
                log_to_file(f"Errore parsing {html_file.name}: {e}")
        save_posts(posts)
        log_to_file("news.json rigenerato da HTML.")
        self.refresh_posts_list()
        messagebox.showinfo("Completato", "news.json rigenerato da HTML.")

def main():
    root = tk.Tk()
    app = BlogManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    def __init__(self, parent, post):
        super().__init__(parent.root)
        self.parent = parent
    self.post = post
    self.title(f"Modifica post: {post.get('title','')}")
    self.geometry("600x600")
    self.resizable(False, False)

    # Variabili
    self.var_title = tk.StringVar(value=post.get('title',''))
    self.var_date = tk.StringVar(value=post.get('date',''))
    self.var_image = tk.StringVar(value=post.get('image',''))
    self.var_summary = tk.StringVar(value=post.get('excerpt',''))

    # Layout
    frm = ttk.Frame(self, padding=20)
    frm.pack(fill='both', expand=True)

    # Titolo
    ttk.Label(frm, text="Titolo:").pack(anchor='w')
    self.entry_title = ttk.Entry(frm, textvariable=self.var_title, font=('Arial', 11))
    self.entry_title.pack(fill='x', pady=5)
    # Data
    ttk.Label(frm, text="Data:").pack(anchor='w')
    self.entry_date = ttk.Entry(frm, textvariable=self.var_date)
    self.entry_date.pack(fill='x', pady=5)

    # Immagine
    ttk.Label(frm, text="Immagine (nome file o percorso):").pack(anchor='w')
    self.entry_image = ttk.Entry(frm, textvariable=self.var_image)
    self.entry_image.pack(fill='x', pady=5)
    # Riassunto
    ttk.Label(frm, text="Riassunto:").pack(anchor='w')
    self.entry_summary = ttk.Entry(frm, textvariable=self.var_summary)
    self.entry_summary.pack(fill='x', pady=5)

    # Contenuto
    ttk.Label(frm, text="Contenuto:").pack(anchor='w')
    self.text_content = scrolledtext.ScrolledText(frm, height=10, font=('Arial', 10))
    self.text_content.pack(fill='both', pady=5)
    self.text_content.insert('1.0', post.get('content',''))

    # Pulsanti
    btn_frame = ttk.Frame(frm)
    btn_frame.pack(fill='x', pady=10)
    ttk.Button(btn_frame, text="Salva", command=self.save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Annulla", command=self.destroy).pack(side='right', padx=5)

    def save(self):
        # Aggiorna dati post
        new_data = {
            'title': self.var_title.get().strip(),
            'date': self.var_date.get().strip(),
            'image': self.var_image.get().strip(),
            'excerpt': self.var_summary.get().strip(),
            'content': self.text_content.get('1.0', 'end').strip(),
        }
        slug = self.post.get('slug')
    update_post(slug, new_data)
    # Aggiorna anche il file HTML associato
    html_path = Path("..", "news", f"{slug}.html")
        if html_path.exists():
            try:
                with open(html_path, "w", encoding="utf-8") as f:
            html = self._render_html(new_data)
            f.write(html)
        except Exception as e:
        messagebox.showerror("Errore", f"Errore aggiornamento file HTML:\n{e}")
    self.parent.refresh_posts_list()
    messagebox.showinfo("Successo", "Post modificato con successo!")
        self.destroy()

    def _render_html(self, data):
        # Semplice template HTML per il post
        html = (
            "<!DOCTYPE html>\n"
            "<html lang='it'>\n"
            "<head>\n"
            "    <meta charset='UTF-8'>\n"
            f"    <title>{data['title']}</title>\n"
            "</head>\n"
            "<body>\n"
            f"    <h1>{data['title']}</h1>\n"
            f"    <p><em>{data['date']}</em></p>\n"
            f"    <img src='../immagini/{data['image']}' alt='Immagine' style='max-width:100%;height:auto;'>\n"
            "    <h3>Riassunto</h3>\n"
            f"    <p>{data['excerpt']}</p>\n"
            "    <hr>\n"
            f"    <div>{data['content'].replace(chr(10),'<br>')}</div>\n"
            "</body>\n"
            "</html>"
        )
        return html

    # ...existing code...

import logging
# === Logging incrementale su file ===
    def log_to_file(message):
    from datetime import datetime
    log_path = Path(__file__).parent / "log_blog_manager.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCS-VV Blog Manager - Versione Migliorata
Applicazione desktop per gestire il blog ARCS-VV con debug migliorato
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.ttk import Notebook
import os

import sys
from datetime import datetime
from pathlib import Path
import webbrowser
import json

# === Finestra di dialogo per modifica post ===
class EditPostDialog(tk.Toplevel):
    def __init__(self, parent, post):
        super().__init__(parent.root)
        self.parent = parent
        self.post = post
        self.title(f"Modifica post: {post.get('title','')}")
        self.geometry("600x600")
        self.resizable(False, False)

        # Variabili
        self.var_title = tk.StringVar(value=post.get('title',''))
        self.var_date = tk.StringVar(value=post.get('date',''))
        self.var_image = tk.StringVar(value=post.get('image',''))
        self.var_summary = tk.StringVar(value=post.get('excerpt',''))

        # Layout
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill='both', expand=True)

        # Titolo
        ttk.Label(frm, text="Titolo:").pack(anchor='w')
        self.entry_title = ttk.Entry(frm, textvariable=self.var_title, font=('Arial', 11))
        self.entry_title.pack(fill='x', pady=5)

        # Data
        ttk.Label(frm, text="Data:").pack(anchor='w')
        self.entry_date = ttk.Entry(frm, textvariable=self.var_date)
        self.entry_date.pack(fill='x', pady=5)

        # Immagine
        ttk.Label(frm, text="Immagine (nome file o percorso):").pack(anchor='w')
        self.entry_image = ttk.Entry(frm, textvariable=self.var_image)
        self.entry_image.pack(fill='x', pady=5)

        # Riassunto
        ttk.Label(frm, text="Riassunto:").pack(anchor='w')
        self.entry_summary = ttk.Entry(frm, textvariable=self.var_summary)
        self.entry_summary.pack(fill='x', pady=5)

        # Contenuto
        ttk.Label(frm, text="Contenuto:").pack(anchor='w')
        self.text_content = scrolledtext.ScrolledText(frm, height=10, font=('Arial', 10))
        self.text_content.pack(fill='both', pady=5)
        self.text_content.insert('1.0', post.get('content',''))

        # Pulsanti
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill='x', pady=10)
    ttk.Button(btn_frame, text="Salva", command=self.save).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Annulla", command=self.destroy).pack(side='right', padx=5)

    def save(self):
        # Aggiorna dati post
        new_data = {
            'title': self.var_title.get().strip(),
            'date': self.var_date.get().strip(),
            'image': self.var_image.get().strip(),
            'excerpt': self.var_summary.get().strip(),
            'content': self.text_content.get('1.0', 'end').strip(),
        }
        slug = self.post.get('slug')
        update_post(slug, new_data)
        # Aggiorna anche il file HTML associato
        html_path = Path("..", "news", f"{slug}.html")
        if html_path.exists():
            try:
                with open(html_path, "w", encoding="utf-8") as f:
                    html = self._render_html(new_data)
                    f.write(html)
            except Exception as e:
                messagebox.showerror("Errore", f"Errore aggiornamento file HTML:\n{e}")
        self.parent.refresh_posts_list()
        messagebox.showinfo("Successo", "Post modificato con successo!")
        self.destroy()

    def _render_html(self, data):
        # Semplice template HTML per il post
        html = (
            "<!DOCTYPE html>\n"
            "<html lang='it'>\n"
            "<head>\n"
            "    <meta charset='UTF-8'>\n"
            f"    <title>{data['title']}</title>\n"
            "</head>\n"
            "<body>\n"
            f"    <h1>{data['title']}</h1>\n"
            f"    <p><em>{data['date']}</em></p>\n"
            f"    <img src='../immagini/{data['image']}' alt='Immagine' style='max-width:100%;height:auto;'>\n"
            "    <h3>Riassunto</h3>\n"
            f"    <p>{data['excerpt']}</p>\n"
            "    <hr>\n"
            f"    <div>{data['content'].replace(chr(10),'<br>')}</div>\n"
            "</body>\n"
            "</html>"
        )
        return html

# === Funzioni locali per gestione post ===
NEWS_JSON_PATH = Path("..", "news", "news.json")
NEWS_HTML_DIR = Path("..", "news")

def load_posts():
    if NEWS_JSON_PATH.exists():
        with open(NEWS_JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(NEWS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def delete_post_by_slug(slug):
    posts = load_posts()
    posts = [p for p in posts if p["slug"] != slug]
    save_posts(posts)
    html_path = NEWS_HTML_DIR / f"{slug}.html"
    if html_path.exists():
        html_path.unlink()
    return True

def get_post_by_slug(slug):
    posts = load_posts()
    for p in posts:
        if p["slug"] == slug:
            return p
    return None

def update_post(slug, new_data):
    posts = load_posts()
    for i, p in enumerate(posts):
        if p["slug"] == slug:
            posts[i].update(new_data)
            break
    save_posts(posts)
    return True

class ARCSBlogManager:
    def __init__(self, root):
        def refresh_posts_list(self):
            """Aggiorna la lista dei post e scrive un log incrementale su file."""
            print("🔄 Aggiornamento lista post...")
            log_to_file("Avvio refresh_posts_list")

            # Pulisce la lista
            for item in self.posts_tree.get_children():
                self.posts_tree.delete(item)

            # Prepara log diagnostico
            log_lines = []
            post_dir = (Path(__file__).parent.parent / "news").resolve()
            log_lines.append(f"Percorso usato: pages/news/")
            log_lines.append(f"Percorso assoluto cartella news: {post_dir}")

            # Verifica se la cartella esiste
            if not post_dir.exists():
                msg = f"❌ La cartella pages/news NON esiste! Percorso controllato: {post_dir}"
                log_lines.append(msg)
                log_to_file(msg)
                try:
                    post_dir.mkdir(parents=True, exist_ok=True)
                    msg2 = f"✅ Cartella creata automaticamente: {post_dir}"
                    log_lines.append(msg2)
                    log_to_file(msg2)
                except Exception as e:
                    msg3 = f"❌ Errore nella creazione della cartella: {e}"
                    log_lines.append(msg3)
                    log_to_file(msg3)
                    self._update_diagnostic_log(log_lines)
                    return

            # Elenco file e diagnostica
            try:
                all_files = list(post_dir.iterdir())
                if all_files:
                    log_lines.append(f"Tutti i file trovati nella cartella:")
                    for f in all_files:
                        log_lines.append(f"- {f.name}")
                else:
                    log_lines.append("⚠️ Nessun file trovato nella cartella.")
                html_files = list(post_dir.glob("*.html"))
                if html_files:
                    log_lines.append(f"File HTML trovati nella cartella:")
                    for f in html_files:
                        log_lines.append(f"- {f.name}")
                else:
                    log_lines.append("⚠️ Nessun file HTML trovato nella cartella.")
            except Exception as e:
                log_lines.append(f"❌ Errore lettura cartella: {e}")
                log_to_file(f"❌ Errore lettura cartella: {e}")

            # Caricamento post
            try:
                posts = load_posts()
                if not posts:
                    messagebox.showinfo("Nessun post trovato", "La lista dei post è vuota.\nVerifica che i file siano nella cartella pages/news.")
                    msg = "⚠️ Nessun post processato come post valido."
                    log_lines.append(msg)
                    log_to_file(msg)
                else:
                    msg = f"✅ {len(posts)} post validi trovati."
                    log_lines.append(msg)
                    log_to_file(msg)
                    log_lines.append("File processati come post:")
                    for post in posts:
                        filename = post.get('slug', '') + '.html'
                        self.posts_tree.insert('', 'end', values=(post.get('date',''), post.get('title',''), filename))
                        log_lines.append(f"- {filename}")
                        log_to_file(f"Post trovato: {filename}")
                    print(f"✅ Lista aggiornata: {len(posts) if posts else 0} post trovati")
            except Exception as e:
                msg = f"❌ Errore caricamento post: {e}"
                messagebox.showerror("Errore", f"Errore nel caricare i post:\n{str(e)}")
                log_lines.append(msg)
                log_to_file(msg)
                print(msg)

            self._update_diagnostic_log(log_lines)

            self._update_diagnostic_log(log_lines)
        # Titolo
        title_frame = ttk.LabelFrame(content_frame, text="📝 Titolo del Post", padding="10")
        title_frame.pack(fill='x', pady=(0, 15))
        
        self.title_entry = ttk.Entry(title_frame, font=('Arial', 11))
        self.title_entry.pack(fill='x')
        
        # Immagine
        image_frame = ttk.LabelFrame(content_frame, text="🖼️ Immagine del Post", padding="10")
        image_frame.pack(fill='x', pady=(0, 15))
        
        image_input_frame = ttk.Frame(image_frame)
        image_input_frame.pack(fill='x')
        
        self.image_entry = ttk.Entry(image_input_frame, textvariable=self.selected_image)
        self.image_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(image_input_frame, text="📁 Sfoglia", command=self.select_image).pack(side='right', padx=(10, 0))
        
        # Riassunto
        summary_frame = ttk.LabelFrame(content_frame, text="📄 Riassunto (per la pagina News)", padding="10")
        summary_frame.pack(fill='x', pady=(0, 15))
        
        self.summary_text = tk.Text(summary_frame, height=4, font=('Arial', 10))
        self.summary_text.pack(fill='x')
        
        # Contenuto
        content_label_frame = ttk.LabelFrame(content_frame, text="📖 Contenuto Completo", padding="10")
        content_label_frame.pack(fill='x', pady=(0, 20))
        
        self.content_text = scrolledtext.ScrolledText(content_label_frame, height=8, font=('Arial', 11))
        self.content_text.pack(fill='x')
        
        print("✅ Tab Nuovo Post costruito con pulsanti visibili")
    
    def delete_post(self):
        """Elimina il post selezionato da news.json e HTML"""
        selection = self.posts_tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un post dalla lista")
            return
        item = self.posts_tree.item(selection[0])
        title = item['values'][1]
        filename = item['values'][2]
        slug = filename.replace('.html','')
        result = messagebox.askyesno(
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare il post?\n\n"
            f"📄 Titolo: {title}\n"
            f"📁 File: {filename}\n\n"
            f"⚠️ Questa operazione NON può essere annullata!"
        )
        if result:
            try:
                delete_post_by_slug(slug)
                messagebox.showinfo("Successo", f"Post '{title}' eliminato con successo")
                self.refresh_posts_list()
                print(f"🗑️ Post eliminato: {title}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nell'eliminazione:\n{str(e)}")
                print(f"❌ Errore eliminazione: {e}")
        self.diagnostic_log.pack(fill='x', expand=True)

        # Pulsanti per la gestione
        manage_frame = ttk.Frame(main_frame)
        manage_frame.pack(fill='x')

        ttk.Button(manage_frame, text="🔄 Aggiorna Lista", command=self.refresh_posts_list).pack(side='left', padx=(0, 10))
        ttk.Button(manage_frame, text="👀 Visualizza", command=self.view_post).pack(side='left', padx=(0, 10))
        ttk.Button(manage_frame, text="🗑️ Elimina", command=self.delete_post).pack(side='right')

        # Carica la lista iniziale
        self.refresh_posts_list()

        print("✅ Tab Gestisci Post costruito")
    
    def build_manage_tab(self):
        """Costruisce la tab Gestisci Post con i pulsanti di gestione"""
        frame = self.manage_tab
        # Pulsanti gestione
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="🔄 Aggiorna Lista", command=self.refresh_posts_list).pack(side='left', padx=(0, 10))
        ttk.Button(btn_frame, text="👀 Visualizza", command=self.view_post).pack(side='left', padx=(0, 10))
        ttk.Button(btn_frame, text="🗑️ Elimina", command=self.delete_post).pack(side='right')
        ttk.Button(btn_frame, text="📝 Rigenera news.json da HTML", command=self.regenerate_news_json).pack(side='left', padx=(0, 10))
    
    def regenerate_news_json(self):
        """Rigenera news.json dai file HTML e aggiorna la lista post."""
        try:
            generate_news_json_from_html()
            self.refresh_posts_list()
            messagebox.showinfo("Successo", "news.json rigenerato dai file HTML.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella rigenerazione di news.json: {e}")
        # Log diagnostico
        self.diagnostic_log.pack(fill='x', expand=True)
        print("✅ Tab Gestisci Post costruito")
    
    def build_help_tab(self):
        """Costruisce il tab di aiuto"""
        print("❓ Costruzione tab Aiuto...")
        
        frame = self.help_tab
        
        # Scroll text per l'aiuto
        help_text = scrolledtext.ScrolledText(frame, wrap='word', font=('Arial', 10))
        help_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        help_content = """
🏠 ARCS-VV Blog Manager - Guida Utente

📝 COME CREARE UN NUOVO POST:

1. 📅 Inserisci la data (o clicca "Oggi")
2. 📝 Scrivi il titolo del post  
3. 🖼️ Seleziona un'immagine (facoltativo)
4. 📄 Scrivi un breve riassunto per la pagina News
5. 📖 Scrivi il contenuto completo del post
6. 👀 Clicca "VISUALIZZA ANTEPRIMA" per controllare
7. ✨ Clicca "CREA BLOG POST" per pubblicare

🎨 FORMATTAZIONE TESTO:
• **testo in grassetto**
• *testo in corsivo*  
• • Elenchi puntati
• 1. Elenchi numerati
• /n per andare a capo forzato

🗑️ GESTIRE POST ESISTENTI:
• Vai al tab "Gestisci Post"
• Seleziona un post dalla lista
• Clicca "Visualizza" per aprirlo nel browser
• Clicca "Elimina" per rimuoverlo (ATTENZIONE: non reversibile!)

🖼️ IMMAGINI:
• Formati supportati: JPG, PNG, GIF, BMP
• Il sistema ridimensiona automaticamente a 800x400px
• Le immagini vengono salvate in immagini/

⚠️ IMPORTANTE:
• Fai sempre l'anteprima prima di pubblicare
• Le eliminazioni non sono reversibili
• Mantieni titoli brevi e descrittivi
• Usa riassunti coinvolgenti per la pagina News

🆘 PROBLEMI COMUNI:
• Se mancano i pulsanti, ingrandisci la finestra
• Se l'immagine non appare, controlla il percorso
• Se il post non si crea, controlla i campi obbligatori

📧 SUPPORTO:
Per problemi tecnici, contatta l'amministratore del sito.
        """
        
        help_text.insert('1.0', help_content)
        help_text.config(state='disabled')
        
        print("✅ Tab Aiuto costruito")
    
    # Metodi per le azioni
    def edit_post(self):
        """Modifica il post selezionato usando update_post"""
        selection = self.posts_tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un post dalla lista")
            return
        item = self.posts_tree.item(selection[0])
        filename = item['values'][2]
        slug = filename.replace('.html','')
        post_to_edit = get_post_by_slug(slug)
        if not self.title_entry.get().strip():
            messagebox.showwarning("Attenzione", "Inserisci un titolo per il post")
            return
        
        if not self.content_text.get("1.0", tk.END).strip():
            messagebox.showwarning("Attenzione", "Inserisci il contenuto del post")
            return
        
        
        try:
            # Dati del post
            date_str = self.post_date.get()
            title = self.title_entry.get().strip()
            image_path = self.selected_image.get().strip() if self.selected_image.get() else ""
            summary = self.summary_text.get("1.0", tk.END).strip()
            content = self.content_text.get("1.0", tk.END).strip()

            # Crea il post
            filename, formatted_date, processed_image = create_blog_post(
                title=title,
                date_str=date_str,
                image_path=image_path,
                content=content,
                excerpt=summary
            )

            # Aggiorna la pagina delle news con i dati corretti
            try:
                update_news_page(title, date_str, processed_image, summary, filename)
                print("✅ Pagina news aggiornata con la miniatura del nuovo post")
            except Exception as e:
                print(f"⚠️ Errore aggiornamento pagina news: {e}")

            # Verifica se il file è stato creato correttamente
            post_path = Path("pages/news") / filename
            if post_path.exists():
                messagebox.showinfo("Successo", f"Post '{title}' creato con successo! La pagina news è stata aggiornata.")
                self.clear_form()
                print(f"✅ Post '{title}' creato")
            else:
                messagebox.showerror("Errore", "Errore nella creazione del post (file non trovato)")
                print("❌ Errore nella creazione del post (file non trovato)")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella creazione del post:\n{str(e)}")
            print(f"❌ Errore: {e}")
    
    def clear_form(self):
        """Pulisce il form"""
        self.title_entry.delete(0, tk.END)
        self.selected_image.set("")
        self.summary_text.delete("1.0", tk.END)
        self.content_text.delete("1.0", tk.END)
        self.post_date.set(datetime.now().strftime("%d/%m/%Y"))
        print("🗑️ Form pulito")
    
    def refresh_posts_list(self):
        """Aggiorna la lista dei post"""
        print("🔄 Aggiornamento lista post...")
    log_to_file("Avvio refresh_posts_list")


        # Pulisce la lista
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

        # Prepara log diagnostico
        log_lines = []
        post_dir = (Path(__file__).parent.parent / "news").resolve()
        log_lines.append(f"Percorso usato: pages/news/")
        log_lines.append(f"Percorso assoluto cartella news: {post_dir}")

        # Verifica se la cartella esiste
        if not post_dir.exists():
            msg = f"❌ La cartella pages/news NON esiste! Percorso controllato: {post_dir}"
            log_lines.append(msg)
            log_to_file(msg)
            try:
                post_dir.mkdir(parents=True, exist_ok=True)
                msg2 = f"✅ Cartella creata automaticamente: {post_dir}"
                log_lines.append(msg2)
                log_to_file(msg2)
            except Exception as e:
                msg3 = f"❌ Errore nella creazione della cartella: {e}"
                log_lines.append(msg3)
                log_to_file(msg3)
                self._update_diagnostic_log(log_lines)
                return
        else:
            try:
                all_files = list(post_dir.iterdir())
                if all_files:
                    log_lines.append(f"Tutti i file trovati nella cartella:")
                    for f in all_files:
                        log_lines.append(f"- {f.name}")
                else:
                    log_lines.append("⚠️ Nessun file trovato nella cartella.")
                html_files = list(post_dir.glob("*.html"))
                if html_files:
                    log_lines.append(f"File HTML trovati nella cartella:")
                    for f in html_files:
                        log_lines.append(f"- {f.name}")
                else:
                    log_lines.append("⚠️ Nessun file HTML trovato nella cartella.")
            except Exception as e:
                log_lines.append(f"❌ Errore lettura cartella: {e}")

        try:
            posts = load_posts()
            if not posts:
                messagebox.showinfo("Nessun post trovato", "La lista dei post è vuota.\nVerifica che i file siano nella cartella pages/news.")
                msg = "⚠️ Nessun post processato come post valido."
                log_lines.append(msg)
                log_to_file(msg)
            else:
                msg = f"✅ {len(posts)} post validi trovati."
                log_lines.append(msg)
                log_to_file(msg)
                log_lines.append("File processati come post:")
                for post in posts:
                    self.posts_tree.insert('', 'end', values=(post['date'], post['title'], post['filename']))
                    log_lines.append(f"- {post['filename']}")
                    log_to_file(f"Post trovato: {post['filename']}")
            print(f"✅ Lista aggiornata: {len(posts) if posts else 0} post trovati")
        except Exception as e:
            msg = f"❌ Errore caricamento post: {e}"
            messagebox.showerror("Errore", f"Errore nel caricare i post:\n{str(e)}")
            log_lines.append(msg)
            log_to_file(msg)
            print(msg)

        self._update_diagnostic_log(log_lines)

    def _update_diagnostic_log(self, lines):
        """Aggiorna il log diagnostico visibile"""
        self.diagnostic_log.config(state='normal')
        self.diagnostic_log.delete('1.0', tk.END)
        self.diagnostic_log.insert('1.0', '\n'.join(lines))
        self.diagnostic_log.config(state='disabled')
    
    def view_post(self):
        """Visualizza il post selezionato nel browser"""
        selection = self.posts_tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un post dalla lista")
            return
        
        item = self.posts_tree.item(selection[0])
        filename = item['values'][2]
        
        # Apri nel browser
        post_path = Path(f"pages/news/{filename}")
        if post_path.exists():
            webbrowser.open(post_path.absolute().as_uri())
            print(f"👀 Post aperto nel browser: {filename}")
        else:
            messagebox.showerror("Errore", f"File non trovato: {filename}")
    
    def delete_post(self):
        """Elimina il post selezionato"""
        selection = self.posts_tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un post dalla lista")
            return
        
        
        item = self.posts_tree.item(selection[0])
        title = item['values'][1]
        filename = item['values'][2]
        
        # Conferma eliminazione
        result = messagebox.askyesno(
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare il post?\n\n"
            f"📄 Titolo: {title}\n"
            f"📁 File: {filename}\n\n"
            f"⚠️ Questa operazione NON può essere annullata!"
        )
        
        if result:
            try:
                # Trova il post completo dalla lista
                posts = load_posts()
                post_to_delete = None
                for post in posts:
                    if post['filename'] == filename:
                        post_to_delete = post
                        break
                
                if post_to_delete and delete_post(post_to_delete):
                    messagebox.showinfo("Successo", f"Post '{title}' eliminato con successo")
                    # Rimuovi il post dalla Treeview senza ricaricare tutta la lista
                    for item_id in self.posts_tree.get_children():
                        item_data = self.posts_tree.item(item_id)
                        if item_data['values'][2] == filename:
                            self.posts_tree.delete(item_id)
                            break
                    print(f"🗑️ Post eliminato: {title}")
                else:
                    messagebox.showerror("Errore", "Errore nell'eliminazione del post")
                    print("❌ Errore nell'eliminazione del post")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nell'eliminazione:\n{str(e)}")
                print(f"❌ Errore eliminazione: {e}")

    def set_today(self):
        """Imposta la data odierna nel campo data"""
        self.post_date.set(datetime.now().strftime("%d/%m/%Y"))

    def select_image(self):
        """Apre una finestra di dialogo per selezionare un file immagine e aggiorna il campo relativo"""
        filetypes = [
            ("Immagini", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("Tutti i file", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Seleziona immagine",
            initialdir=".",
            filetypes=filetypes
        )
        if filename:
            self.selected_image.set(filename)

def main():
    """Funzione principale"""
    print("🚀 Avvio ARCS-VV Blog Manager...")
    
    root = tk.Tk()
    app = ARCSBlogManager(root)
    
    print("🎉 Applicazione avviata con successo!")
    root.mainloop()

if __name__ == "__main__":
    main()

def generate_news_json_from_html():
    """Genera news.json a partire dai file HTML trovati in pages/news, estraendo tutti i dati possibili."""
    import re
    html_dir = Path("..", "news")
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
            # Estrai contenuto (tutto tra <body>...</body>)
            full_content = None
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
            print(f"Errore lettura {html_file}: {e}")
    save_posts(news)
    print(f"news.json rigenerato con {len(news)} post trovati in HTML.")

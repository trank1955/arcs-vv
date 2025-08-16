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
import subprocess
import sys

# === Logging incrementale su file ===
def log_to_file(message):
    log_path = Path(__file__).parent / "log_blog_manager.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# === Percorsi centralizzati ===
try:
    from config_paths import NEWS_JSON_PATH, NEWS_DIR
except Exception as e:
    # Fallback relativo (non dovrebbe servire)
    NEWS_JSON_PATH = Path("..", "news", "news.json")
    NEWS_DIR = Path("..", "news")
    log_to_file(f"[WARN] config_paths import fallito: {e}")

BACKUP_DIR = NEWS_DIR / "backups"

# === Funzioni locali per gestione post ===

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


def regenerate_news_pages():
    """Richiama genera_news.py per rigenerare index e dettagli in base ai template."""
    script_path = Path(__file__).parent / "genera_news.py"
    try:
        result = subprocess.run([sys.executable, str(script_path)], input="n\n", text=True, capture_output=True)
        if result.returncode != 0:
            log_to_file(f"[ERR] genera_news.py failed: {result.stderr}")
            messagebox.showerror("Errore", f"Rigenerazione news fallita:\n{result.stderr}")
        else:
            log_to_file("Rigenerazione news completata.")
    except Exception as e:
        log_to_file(f"[ERR] Exception genera_news.py: {e}")
        messagebox.showerror("Errore", f"Eccezione durante la rigenerazione:\n{e}")


def delete_post_by_slug(slug):
    posts = load_posts()
    posts = [p for p in posts if p["slug"] != slug]
    save_posts(posts)
    html_path = NEWS_DIR / f"{slug}.html"
    if html_path.exists():
        try:
            html_path.unlink()
            log_to_file(f"File HTML eliminato: {html_path}")
        except Exception as e:
            log_to_file(f"Errore eliminazione HTML: {e}")
            return False
    # Rigenera lista/index dopo eliminazione
    regenerate_news_pages()
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
    html_dir = NEWS_DIR
    news = []
    for html_file in html_dir.glob("*.html"):
        try:
            with open(html_file, encoding="utf-8") as f:
                content = f.read()
            # Estrazioni basilari
            title = None
            m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if m:
                title = m.group(1).strip()
            else:
                m = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE)
                if m:
                    title = m.group(1).strip()
            date = None
            m = re.search(r'<meta[^>]*name=["\']?date["\']?[^>]*content=["\']?([\d\-/]+)["\']?', content, re.IGNORECASE)
            if m:
                date = m.group(1)
            author = None
            m = re.search(r'<meta[^>]*name=["\']?author["\']?[^>]*content=["\']?([^"\'>]+)["\']?', content, re.IGNORECASE)
            if m:
                author = m.group(1).strip()
            image = None
            m = re.search(r'<img[^>]*src=["\']([^"\'>]+)["\']', content, re.IGNORECASE)
            if m:
                image = m.group(1).strip()
            excerpt = None
            m = re.search(r'<h3>\s*Riassunto\s*</h3>\s*<p>(.*?)</p>', content, re.IGNORECASE|re.DOTALL)
            if m:
                excerpt = m.group(1).strip()
            else:
                m = re.search(r'<p>(.*?)</p>', content, re.IGNORECASE|re.DOTALL)
                if m:
                    excerpt = m.group(1).strip()
            full_content = None
            hr_match = re.search(r'<hr[^>]*>', content, re.IGNORECASE)
            if hr_match:
                hr_end = hr_match.end()
                body_close = content.find('</body>', hr_end)
                if body_close != -1:
                    full_content = content[hr_end:body_close].strip()
            else:
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

    def browse_image(self):
        initial_dir = (NEWS_DIR.parent / "immagini").resolve()
        file_path = filedialog.askopenfilename(
            initialdir=str(initial_dir),
            title="Seleziona immagine",
            filetypes=(("Immagini", "*.jpg *.jpeg *.png *.gif"), ("Tutti i file", "*.*"))
        )
        if file_path:
            # Crea percorso relativo rispetto alla radice sito
            try:
                rel_path = Path(file_path).resolve().relative_to(NEWS_DIR.parent.parent)
                self.var_image.set(str(rel_path).replace('\\', '/'))
            except Exception:
                # Fallback: relativo a pages
                rel_path = Path(file_path).resolve().relative_to(NEWS_DIR.parent)
                self.var_image.set(str(rel_path).replace('\\', '/'))

    def preview(self):
        """Mostra anteprima HTML minimale in browser"""
        temp_path = Path("temp_preview.html")
        try:
            html_content = self._render_html(self._get_form_data())
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
            'excerpt': self.entry_summary.get('1.0', 'end').strip(),
            'content': self.text_content.get('1.0', 'end').strip(),
        }

    def save(self):
        data = self._get_form_data()
        slug = self.post.get('slug')
        
        # Verifica esistenza immagine solo se relativa alla cartella immagini
        if data['image'] and not (str(data['image']).startswith('http') or str(data['image']).startswith('../')):
            img_path = NEWS_DIR.parent / 'immagini' / data['image']
            if not img_path.exists():
                if not messagebox.askyesno(
                    "Immagine mancante",
                    f"File immagine non trovato:\n{img_path}\n\nVuoi continuare comunque?"
                ):
                    return
        
        # Aggiorna dati post e rigenera pagine
        update_post(slug, data)
        regenerate_news_pages()
        self.parent.refresh_posts_list()
        messagebox.showinfo("Successo", "Post modificato con successo!")
        self.destroy()

    def _render_html(self, data):
        # Anteprima semplice (non usata per salvataggio)
        return f"""<!DOCTYPE html>
<html lang='it'>
<head>
    <meta charset='UTF-8'>
    <title>{html.escape(data['title'])}</title>
</head>
<body>
    <h1>{html.escape(data['title'])}</h1>
    <p><em>{html.escape(data['date'])}</em></p>
    <div>{data['content']}</div>
</body>
</html>"""

# === MAIN APP ===
class BlogManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ARCS-VV Blog Manager")
        try:
            self.root.state('zoomed')  # Avvio a tutto schermo su Windows
        except Exception:
            pass

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

        # Lista post (con barra di scorrimento)
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
        ttk.Button(btn_frame, text="Modifica", command=self.edit_selected_post).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Elimina", command=self.delete_selected_post).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Apri HTML", command=self.open_html_selected_post).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_posts_list).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Rigenera news.json", command=self.generate_news_json_from_html).pack(side=tk.RIGHT, padx=5)

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
        html_files = {f.stem for f in NEWS_DIR.glob("*.html")}
        
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
        # Implementazione semplificata per creazione nuovo post
        slug = datetime.now().strftime("post_%Y%m%d%H%M%S")
        new_post = {
            'title': "Nuovo Post",
            'slug': slug,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'author': "ARCS-VV",
            'content': "<p>Inserisci il contenuto qui</p>"
        }
        
        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)
        regenerate_news_pages()
        
        # Crea file HTML vuoto (opzionale: ora viene rigenerato dai template)
        try:
            html_path = NEWS_DIR / f"{slug}.html"
            if not html_path.exists():
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write("<h1>Nuovo Post</h1>")
        except Exception:
            pass
        
        self.refresh_posts_list()
        messagebox.showinfo("Successo", f"Nuovo post creato: {slug}")

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
        html_path = NEWS_DIR / f"{slug}.html"
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
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path
import re
from config_paths import BASE_DIR, TEMPLATES_DIR, NEWS_JSON_PATH, NEWS_DIR


def slugify(title: str) -> str:
	import re
	slug = re.sub(r'[^\w\s-]', '', title.lower())
	slug = re.sub(r'[-\s]+', '-', slug)
	return slug.strip('-')


def sanitize_content(raw: str) -> str:
	if not raw:
		return ''
	# Estrai contenuto interno al blocco blog-content se presente
	m = re.search(r'<div\s+class=["\']blog-content["\']>([\s\S]*?)</div>', raw, re.IGNORECASE)
	if m:
		return m.group(1).strip()
	# Se c'è un <hr>, prendi tutto dopo
	hr = re.search(r'<hr[^>]*>', raw, re.IGNORECASE)
	if hr:
		return raw[hr.end():].strip()
	# Fallback: corpo del body
	m = re.search(r'<body[^>]*>([\s\S]*?)</body>', raw, re.IGNORECASE)
	if m:
		return m.group(1).strip()
	# Ultimo fallback: restituisci raw
	return raw.strip()


def strip_tags(html: str) -> str:
	return re.sub(r'<[^>]+>', '', html or '').strip()


def normalize_posts(posts: list) -> list:
	normalized = []
	for p in posts:
		post = dict(p)
		post.setdefault('author', 'ARCS-VV')
		post.setdefault('date', '')
		post.setdefault('title', post.get('slug', ''))
		# Pulisci contenuto da layout completo eventualmente incollato
		post['content'] = sanitize_content(post.get('content', ''))
		# Excerpt: se mancante o è solo il link "torna all'elenco", crea un riassunto testuale
		excerpt = (post.get('excerpt') or '').strip()
		if not excerpt or excerpt.lower().startswith('<a ') or len(strip_tags(excerpt)) < 10:
			text = strip_tags(post['content'])
			post['excerpt'] = (text[:220] + '...') if len(text) > 220 else text
		normalized.append(post)
	# Ordina per data desc se possibile
	def parse_date(d: str):
		try:
			return datetime.strptime(d, '%Y-%m-%d')
		except Exception:
			return datetime.min
	return sorted(normalized, key=lambda x: parse_date(x.get('date', '')), reverse=True)


def add_new_post(posts: list):
	print("\n--- Nuovo post news ---")
	title = input("Titolo: ").strip()
	slug = slugify(title)
	date = input(f"Data (YYYY-MM-DD) [default: oggi]: ").strip() or datetime.now().strftime('%Y-%m-%d')
	author = input("Autore [default: ARCS-VV]: ").strip() or "ARCS-VV"
	excerpt = input("Estratto: ").strip()
	print("Inserisci il contenuto HTML (termina con una riga vuota):")
	lines = []
	while True:
		line = input()
		if line == '':
			break
		lines.append(line)
	content = '\n'.join(lines)
	youtube = []
	pdf = []
	if input("Aggiungere video YouTube? (s/n): ").lower() == 's':
		while True:
			url = input("URL (invio per terminare): ").strip()
			if not url:
				break
			youtube.append(url)
	if input("Aggiungere PDF? (s/n): ").lower() == 's':
		while True:
			fname = input("Nome file PDF (invio per terminare): ").strip()
			if not fname:
				break
			pdf.append(fname)
	post = {
		"title": title,
		"slug": slug,
		"date": date,
		"author": author,
		"excerpt": excerpt,
		"content": content,
		"youtube": youtube,
		"pdf": pdf
	}
	posts.insert(0, post)
	print(f"Aggiunto post: {title} (slug: {slug})")


def main():
	NEWS_DIR.mkdir(parents=True, exist_ok=True)
	# Carica i dati dei post
	if NEWS_JSON_PATH.exists():
		with NEWS_JSON_PATH.open(encoding='utf-8') as f:
			raw_posts = json.load(f)
	else:
		raw_posts = []

	# Modalità interattiva per aggiungere una nuova news
	if input("Vuoi aggiungere una nuova news? (s/n): ").lower() == 's':
		add_new_post(raw_posts)
		# Salva news.json aggiornato
		with NEWS_JSON_PATH.open('w', encoding='utf-8') as f:
			json.dump(raw_posts, f, ensure_ascii=False, indent=2)
		print("news.json aggiornato.")

	# Normalizza e ordina post per la generazione
	posts = normalize_posts(raw_posts)

	# Setup Jinja2
	env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
	news_index_template = env.get_template('news.html')
	news_post_template = env.get_template('news_template.html')

	# Genera la pagina indice delle news
	news_index_file = BASE_DIR / 'pages' / 'news.html'
	with news_index_file.open('w', encoding='utf-8') as f:
		f.write(news_index_template.render(posts=posts))

	# Genera una pagina per ogni post in pages/news
	for post in posts:
		out_path = NEWS_DIR / f"{post['slug']}.html"
		with out_path.open('w', encoding='utf-8') as f:
			f.write(news_post_template.render(post=post))

	print("News generate correttamente!")


if __name__ == "__main__":
	main()

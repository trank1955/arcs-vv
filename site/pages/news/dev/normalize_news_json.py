#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime
from pathlib import Path
from config_paths import NEWS_JSON_PATH, NEWS_DIR

BACKUP_DIR = NEWS_DIR / 'backups'

DATE_PATTERNS = [
	# 2025-08-09
	r'^(?P<y>\d{4})[-/.](?P<m>\d{1,2})[-/.](?P<d>\d{1,2})$',
	# 09/08/2025
	r'^(?P<d>\d{1,2})[-/.](?P<m>\d{1,2})[-/.](?P<y>\d{4})$',
]


def parse_date_any(s: str) -> str:
	if not s:
		return ''
	s = s.strip()
	for pat in DATE_PATTERNS:
		m = re.match(pat, s)
		if m:
			try:
				y = int(m.group('y'))
				mth = int(m.group('m'))
				dy = int(m.group('d'))
				return datetime(y, mth, dy).strftime('%Y-%m-%d')
			except Exception:
				pass
	return ''


def slugify(title: str) -> str:
	slug = re.sub(r'[^\w\s-]', '', (title or '').lower())
	slug = re.sub(r'[-\s]+', '-', slug)
	return slug.strip('-')


def strip_tags(html: str) -> str:
	return re.sub(r'<[^>]+>', '', html or '').strip()


def sanitize_content(raw: str) -> str:
	if not raw:
		return ''
	m = re.search(r'<div\s+class=["\']blog-content["\']>([\s\S]*?)</div>', raw, re.IGNORECASE)
	if m:
		return m.group(1).strip()
	hr = re.search(r'<hr[^>]*>', raw, re.IGNORECASE)
	if hr:
		return raw[hr.end():].strip()
	m = re.search(r'<body[^>]*>([\s\S]*?)</body>', raw, re.IGNORECASE)
	if m:
		return m.group(1).strip()
	return raw.strip()


def main():
	# Backup
	BACKUP_DIR.mkdir(parents=True, exist_ok=True)
	if NEWS_JSON_PATH.exists():
		backup_path = BACKUP_DIR / ("news_normalize_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".json")
		backup_path.write_text(NEWS_JSON_PATH.read_text(encoding='utf-8'), encoding='utf-8')

	# Carica
	posts = json.loads(NEWS_JSON_PATH.read_text(encoding='utf-8')) if NEWS_JSON_PATH.exists() else []
	normalized = []
	seen_slugs = set()
	for p in posts:
		post = dict(p)
		post['title'] = (post.get('title') or '').strip()
		post['date'] = parse_date_any(post.get('date', '')) or post.get('date', '')
		post['author'] = post.get('author') or 'ARCS-VV'
		# slug
		slug = (post.get('slug') or slugify(post['title']) or 'post-' + datetime.now().strftime('%Y%m%d%H%M%S'))
		# uniquify
		base = slug
		idx = 2
		while slug in seen_slugs:
			slug = f"{base}-{idx}"
			idx += 1
		seen_slugs.add(slug)
		post['slug'] = slug
		# content
		post['content'] = sanitize_content(post.get('content', ''))
		# excerpt
		excerpt = (post.get('excerpt') or '').strip()
		if not excerpt or excerpt.lower().startswith('<a ') or len(strip_tags(excerpt)) < 10:
			text = strip_tags(post['content'])
			post['excerpt'] = (text[:220] + '...') if len(text) > 220 else text
		normalized.append(post)

	# Ordina per data desc se possibile (vuote in coda)
	def key_date(p):
		try:
			return datetime.strptime(p.get('date',''), '%Y-%m-%d')
		except Exception:
			return datetime.min
	normalized.sort(key=key_date, reverse=True)

	# Salva
	NEWS_JSON_PATH.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding='utf-8')
	print(f"Normalizzazione completata. Post: {len(normalized)}\nBackup: {backup_path}")

if __name__ == '__main__':
	main()
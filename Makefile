PY=python3

.PHONY: news deploy all serve clean

news:
	$(PY) tools/update_news.py

deploy:
	$(PY) tools/deploy_all.py

all: news deploy

serve:
	$(PY) -m http.server --directory public 8000

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} + ; \
	find . -type f -name "*.pyc" -delete ; \
	rm -f temp_preview.html pages/news/temp_preview.html tools/blog_manager/log_blog_manager.txt || true

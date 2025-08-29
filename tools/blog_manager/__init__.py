# Blog Manager Module per ARCS-VV
from .blog_manager import (
    NewsArticle,
    slugify,
    extract_news_from_html,
    generate_news_json_from_html,
    create_news_article,
    update_news_page
)

__all__ = [
    'NewsArticle',
    'slugify', 
    'extract_news_from_html',
    'generate_news_json_from_html',
    'create_news_article',
    'update_news_page'
]

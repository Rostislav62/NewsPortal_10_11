# Путь: NewsPortal/news/utils.py

from django.core.cache import cache

def get_article_cache_key(article_id, publication_date):
    """
    Создаёт уникальный ключ для кэширования статьи на основе её ID и даты последнего изменения.
    """
    return f"article_{article_id}_{publication_date}"





# Путь: your_project/__init__.py
from __future__ import absolute_import, unicode_literals

# Импортируем Celery-приложение
from .celery import app as celery_app

# Указываем, что celery_app доступен для импорта
__all__ = ('celery_app',)

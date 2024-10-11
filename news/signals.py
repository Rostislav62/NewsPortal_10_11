# Путь: NewsPortal/news/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.cache import cache
from .models import Article  # Импорт модели Article
from .utils import get_article_cache_key  # Импорт функции для получения ключа кэша


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


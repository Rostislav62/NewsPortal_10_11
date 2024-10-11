# Путь: news/tasks.py
from datetime import timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from celery import shared_task
from django.conf import settings
from .email_utils import EmailContentBuilder, send_custom_email  # Импортируем EmailContentBuilder из нового модуля
from django.core.mail import send_mail
from django.core.mail import get_connection
from .models import Article, Category, User  # Импортируем необходимые модели

from datetime import datetime, timedelta

@shared_task
def send_new_article_notification(article_id, use_console_backend=False):
    # Получаем статью
    article = Article.objects.get(id=article_id)

    # Используем правильный EMAIL_BACKEND в зависимости от флага use_console_backend
    email_backend = settings.EMAIL_BACKEND_CONSOLE if use_console_backend else settings.EMAIL_BACKEND_SMTP
    connection = get_connection(backend=email_backend)

    # Получаем всех подписчиков категории статьи
    subscribers = article.category.subscribers.all()

    # Генерируем письмо и отправляем каждому подписчику
    for subscriber in subscribers:
        subject, message = EmailContentBuilder.generate_notification_email(article, subscriber)
        send_mail(subject, message, settings.EMAIL_HOST_USER, [subscriber.email], connection=connection)

    return f"Notification sent to {len(subscribers)} subscribers."


# Функция для отправки еженедельного дайджеста подписчикам категорий
def send_weekly_digest():
    """
    Отправка еженедельного дайджеста подписчикам категорий.
    """
    one_week_ago = timezone.now() - timedelta(days=7)

    # Находим все категории, в которых появились новые статьи за последнюю неделю
    categories_with_new_articles = Category.objects.filter(
        article__publication_date__gte=one_week_ago
    ).distinct()

    for category in categories_with_new_articles:
        # Получаем всех подписчиков данной категории
        subscribers = category.subscribers.all()

        # Формируем список новых статей
        new_articles = Article.objects.filter(
            category=category,
            publication_date__gte=one_week_ago
        )

        # Генерация содержимого письма
        subject, message = EmailContentBuilder.generate_weekly_digest_email(category, new_articles)

        # Отправляем письмо каждому подписчику
        for subscriber in subscribers:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscriber.email],
                fail_silently=False
            )


# Функция для отправки ежедневного дайджеста
def send_daily_digest():
    """
    Отправка ежедневного дайджеста подписчикам категорий.
    """
    one_day_ago = timezone.now() - timedelta(days=1)

    # Находим все категории, в которых появились новые статьи за последний день
    categories_with_new_articles = Category.objects.filter(
        article__publication_date__gte=one_day_ago
    ).distinct()

    for category in categories_with_new_articles:
        # Получаем всех подписчиков данной категории
        subscribers = category.subscribers.all()

        # Формируем список новых статей
        new_articles = Article.objects.filter(
            category=category,
            publication_date__gte=one_day_ago
        )

        # Генерация содержимого письма
        subject, message = EmailContentBuilder.generate_weekly_digest_email(category, new_articles)

        # Отправляем письмо каждому подписчику
        for subscriber in subscribers:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscriber.email],
                fail_silently=False
            )


def start_scheduler():
    """
    Функция для запуска планировщика и регистрации задач.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # # Регистрируем задачу с помощью cron: каждое воскресенье в 00:00 (еженедельный дайджест)
    # scheduler.add_job(
    #     send_weekly_digest,
    #     trigger=CronTrigger(day_of_week='sun', hour=0, minute=0),
    #     id="weekly_digest",
    #     name="Отправка еженедельного дайджеста",
    #     replace_existing=True,
    # )
    #
    # # Регистрируем задачу с интервалом: каждые 24 часа (ежедневный дайджест)
    # scheduler.add_job(
    #     send_daily_digest,
    #     trigger=IntervalTrigger(days=1),
    #     id="daily_digest",
    #     name="Отправка ежедневного дайджеста",
    #     replace_existing=True,
    # )
# для тестирования ***********************************************************
    scheduler.add_job(
        send_daily_digest,
        trigger="interval",
        minutes=1,  # Интервал в 1 минуту для быстрого тестирования
        id="daily_digest",
        replace_existing=True,
    )

    scheduler.add_job(
        send_weekly_digest,
        trigger="cron",
        day_of_week="*",
        hour=13,  # Текущий час
        minute=(timezone.now().minute + 1) % 60,  # Через 1 минуту от текущего времени
        id="weekly_digest",
        replace_existing=True,
    )

    # для тестирования ***********************************************************



    # Регистрируем события для планировщика и запускаем его
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started!\nПланировщик запущен!")



@shared_task
def add(x, y):
    return x + y




@shared_task
def send_test_email():
    """
    Пример простой задачи, которая отправляет тестовое письмо.
    """
    subject = 'Тестовая задача Celery'
    message = 'Это тестовое письмо, чтобы проверить работу Celery и планировщика задач.'
    recipient_list = ['your_email@example.com']  # Замените на ваш email для теста

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
    print("Тестовое письмо отправлено!")



@shared_task
def send_weekly_digest():
    """
    Еженедельная задача Celery для отправки рассылки с новыми статьями.
    """
    # Получаем дату начала предыдущей недели
    last_week = datetime.now() - timedelta(days=7)

    # Проходим по всем категориям и выбираем новые статьи за последнюю неделю
    for category in Category.objects.all():
        # Находим все статьи, опубликованные в течение последней недели в данной категории
        new_articles = Article.objects.filter(category=category, publication_date__gte=last_week)

        # Если нет новых статей, пропускаем данную категорию
        if not new_articles.exists():
            continue

        # Генерируем содержание письма с помощью метода generate_weekly_digest_email
        subject, message = EmailContentBuilder.generate_weekly_digest_email(category, new_articles)

        # Получаем список подписчиков этой категории
        subscribers = category.subscribers.all()  # Получаем всех пользователей, подписанных на категорию
        recipient_list = [subscriber.email for subscriber in subscribers]

        # Если есть подписчики, отправляем им письмо
        if recipient_list:
            send_custom_email(subject, message, recipient_list, use_console_backend=settings.USE_CONSOLE_EMAIL_BACKEND)
# Путь: NewsPortal/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab  # Импортируем crontab для настройки расписания



# Устанавливаем переменную окружения для Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

# Создаем экземпляр приложения Celery
app = Celery('NewsPortal')

# Загружаем конфигурацию из Django settings, используя префикс 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим и регистрируем задачи в файлах tasks.py в каждом установленном приложении
app.autodiscover_tasks()

# Добавляем конфигурацию worker_pool для режима 'solo'
app.conf.update(
    worker_pool='solo'  # Используем 'solo' в качестве метода pool
)

# Простая задача для проверки работоспособности
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Настраиваем планировщик для Celery Beat
app.conf.beat_schedule = {
    'send-weekly-newsletter-every-monday': {
        'task': 'news.tasks.send_weekly_digest',  # Название задачи
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Запуск каждый понедельник в 8:00 утра
        'args': (),  # Аргументы для задачи, если необходимо
    },
}
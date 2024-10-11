# Путь: NewsPortal/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
# Периодические задачи Celery
from celery.schedules import crontab

# Загрузка переменных из .env файла
load_dotenv()

# Определение BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Использование переменных окружения из .env
SECRET_KEY = os.getenv('SECRET_KEY')

# Конфигурация для аутентификации Google
# SOCIAL_AUTH_GOOGLE_CLIENT_ID = os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
# SOCIAL_AUTH_GOOGLE_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_SECRET')

# Конфигурация для аутентификации Yandex
SOCIAL_AUTH_YANDEX_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_KEY')
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_SECRET')

# Email конфигурация из .env файла
USE_CONSOLE_EMAIL_BACKEND = os.getenv('USE_CONSOLE_EMAIL_BACKEND') == 'True'
# EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_BACKEND_CONSOLE = os.getenv('EMAIL_BACKEND_CONSOLE')
EMAIL_BACKEND_SMTP = os.getenv('EMAIL_BACKEND_SMTP')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') == 'True'
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'False'
# Условие на основе значения USE_CONSOLE_EMAIL_BACKEND
EMAIL_BACKEND = EMAIL_BACKEND_CONSOLE if USE_CONSOLE_EMAIL_BACKEND else EMAIL_BACKEND_SMTP

WELCOME_EMAIL_VARIANT = int(os.getenv('WELCOME_EMAIL_VARIANT', 1))  # Значение по умолчанию - 1


DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'news',
    'django_filters',
    'django.contrib.sites',

# The following apps are required:
    'django.contrib.auth',
    'django.contrib.messages',

    'allauth',
    'allauth.account',

    # Optional -- requires install using `django-allauth[socialaccount]`.
    'allauth.socialaccount',

    'allauth.socialaccount.providers.yandex',  # Для Yandex
    # 'allauth.socialaccount.providers.google', # Для Google
    # 'allauth.socialaccount.providers.facebook',  # Для Facebook
    'django_extensions',
    'django_apscheduler',
    'django_celery_beat',
    'django_celery_results'
]

SITE_ID = 1


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Настройки allauth
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = '/profile/'  # Перенаправление после входа


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'NewsPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Папка для пользовательских шаблонов
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # `allauth` needs this from django
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]


WSGI_APPLICATION = 'NewsPortal.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



SOCIALACCOUNT_PROVIDERS = {
    # 'google': {
    #     'APP': {
    #         'client_id': SOCIAL_AUTH_GOOGLE_CLIENT_ID,
    #         'secret': SOCIAL_AUTH_GOOGLE_SECRET,
    #         'key': ''
    #     }
    # },
    'yandex': {
        'APP': {
            'client_id': SOCIAL_AUTH_YANDEX_OAUTH2_KEY,
            'secret': SOCIAL_AUTH_YANDEX_OAUTH2_SECRET,
            'key': ''
        }
    }
}



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Путь к папке, где будут храниться статические файлы
STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / "static", ] # Путь к папке static в корне проекта

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
SITE_URL = 'http://127.0.0.1:8000'  # базовый URL с портом

# формат даты, которую будет воспринимать наш задачник
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Формат отображения даты в логах

# если задача не выполняется за 25 секунд, то она автоматически снимается,
# можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'apscheduler': {    # Логгер для задач
            'handlers': ['console'], # Отправляем сообщения в консоль
            'level': 'DEBUG',
            'propagate': True,  # Чтобы сообщения также передавались другим логгерам
        },
        'news.custom_cache': {  # Логгер для кэширования
            'handlers': ['console'],  # Отправляем сообщения в консоль
            'level': 'DEBUG',
            'propagate': False,  # Не передавать сообщения другим логгерам
        },
    },
}



# Настройки Celery
# Опция для управления использованием Celery
USE_CELERY = True  # Установите False, если хотите использовать синхронные уведомления

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'  # Адрес брокера сообщений Redis
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # Хранилище результатов выполнения задач
# Если вы хотите использовать RabbitMQ, замените строку на:
# CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
# CELERY_RESULT_BACKEND = 'django-db'  # Хранение результатов в базе данных
# Хранилище результатов задач (например, Redis или другой бекенд)
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_CACHE_BACKEND = 'django-cache'  # Хранение кэшированных данных в Django
CELERY_ACCEPT_CONTENT = ['json']  # Допустимый формат данных
CELERY_TASK_SERIALIZER = 'json'  # Сериализация задач
CELERY_RESULT_SERIALIZER = 'json'  # Сериализация результатов
CELERY_TIMEZONE = 'UTC'  # Временная зона


# модуль, где находятся задачи
CELERY_IMPORTS = (
    'news.tasks',  # Например, ваше приложение `news`
)


# Настройки периодических задач
CELERY_BEAT_SCHEDULE = {
    # 'add-every-30-seconds': {
    #     'task': 'news.tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16)
    # },
    # 'send-test-email-every-minute': {
    #     'task': 'news.tasks.send_test_email',
    #     'schedule': 60.0,  # Выполняется каждую минуту
    # },
    'send-weekly-digest-every-monday-8am': {
        'task': 'news.tasks.send_weekly_digest',  # Путь к задаче
        # 'schedule': crontab(hour=8, minute=0, day_of_week='monday'),  # Каждый понедельник в 8:00 утра
        # 'schedule': crontab(hour=17, minute=7, day_of_week='monday'),  # Каждый понедельник в 17:07
        # 'schedule': crontab(hour=8, minute=0) # Каждый день в 8:00 утра
        # 'schedule': crontab(minute='*/15') # Каждые 15 минут
        # 'schedule': crontab(hour=12, minute=0, day_of_week='fri', month_of_year='1,12') # Каждую первую и последнюю пятницу месяца в 12:00 дня

        'schedule': crontab(minute='*/1') # Каждые 1 минут:

    },
}

CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache', # Стандартные инструменты django
        'BACKEND': 'news.custom_cache.LoggingFileBasedCache',  # Указываем путь до кастомного кэша
        'LOCATION': os.path.join(BASE_DIR, 'cache'),  # Путь к директории для хранения кэша
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        },
    },
    'redis_cache': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}


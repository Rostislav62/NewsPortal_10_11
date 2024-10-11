# *************************************************
# emails_utills.py
# Импорт необходимых модулей
from NewsPortal import settings
from django.core.mail import send_mail, get_connection
from django.conf import settings



class EmailContentBuilder:
    """
    Класс для создания содержимого писем.
    """

    @staticmethod
    def generate_welcome_email(user, variant=1):
        """
        Создаёт приветственное письмо для пользователя.

        Аргументы:
        - `user`: Объект пользователя (User), для которого создаётся письмо.
        - `variant`: Номер варианта письма (1, 2 или 3).

        Варианты:
        1. Приветственное сообщение и ссылка на активацию.
        2. Полное содержание профиля (логин, пароль, имя, фамилия, email, дата регистрации, группы и статус активации).
        3. Полное содержание профиля (логин, пароль, имя и фамилия).
        """
        subject = "Добро пожаловать на наш сайт!"

        if variant == 1:
            message = f"Здравствуй, {user.username}!\n\nСпасибо за регистрацию на нашем сайте. Пожалуйста, активируйте свой аккаунт, перейдя по следующей ссылке:\n\nhttp://127.0.0.1:8000/activate/{user.pk}/\n\nС уважением,\nКоманда сайта"
        elif variant == 2:
            message = (f"Здравствуй, {user.first_name} {user.last_name}!\n\n"
                       f"Спасибо за регистрацию на нашем сайте. Пожалуйста, активируйте свой аккаунт, перейдя по следующей ссылке:\n\n"
                       f"http://127.0.0.1:8000/activate/{user.pk}/\n\n"
                       f"Ваш профиль:\n"
                       f"Логин: {user.username}\n"
                       f"Email: {user.email}\n"
                       f"Дата регистрации: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}\n"
                       f"Группы: {', '.join([group.name for group in user.groups.all()])}\n"
                       f"Статус активации: {'Активен' if user.is_active else 'Не активен'}\n\n"
                       f"С уважением,\nКоманда сайта")
        elif variant == 3:
            message = (f"Здравствуй, {user.first_name} {user.last_name}!\n\n"
                       f"Спасибо за регистрацию на нашем сайте. Пожалуйста, активируйте свой аккаунт, перейдя по следующей ссылке:\n\n"
                       f"http://127.0.0.1:8000/activate/{user.pk}/\n\n"
                       f"Ваш профиль:\n"
                       f"Логин: {user.username}\n"
                       f"Пароль: {user.password} (пожалуйста, смените его после первого входа)\n\n"
                       f"С уважением,\nКоманда сайта")
        else:
            raise ValueError("Invalid variant specified for welcome email generation.")

        return subject, message

    @staticmethod
    def generate_subscription_email(user, category):
        """
        Создаёт письмо для уведомления пользователя о подписке на категорию.

        Аргументы:
        - `user`: Объект пользователя (User), который подписывается.
        - `category`: Объект категории (Category), на которую происходит подписка.
        """
        subject = f"Подписка на категорию {category.name}"
        message = f"Здравствуй, {user.username}!\n\nВы успешно подписались на категорию \"{category.name}\".\nС уважением,\nКоманда сайта."
        return subject, message

    @staticmethod
    def generate_notification_email(article, subscriber=None):
        """
        Создаёт письмо-уведомление для подписчиков о новой статье в категории.

        Аргументы:
        - `article`: Объект статьи (Article), о которой будет отправлено уведомление.
        - `subscriber`: Объект пользователя (User), которому будет отправлено письмо (для персонализированного приветствия).
        """
        category = article.category
        subject = article.title

        # Используем имя и фамилию подписчика, если они указаны, иначе используем "Здравствуй!"
        greeting = f"Здравствуй, {subscriber.first_name} {subscriber.last_name}!" if subscriber else "Здравствуй!"

        # Формируем краткое содержание письма
        message = (f"{greeting}\n\n"
                   f"В разделе {category.name} появилась новая публикация:\n\n"
                   f"Название: {article.title}\n"
                   f"Автор: {article.author_profile.user.get_full_name() or article.author_profile.user.username}\n\n"
                   f"Краткое содержание:\n"
                   f"{article.content[:50]}...\n\n"
                   f"Перейдите по ссылке, чтобы прочитать полностью: http://127.0.0.1:8000/news/{article.pk}\n\n"
                   f"С уважением,\n"
                   f"Команда сайта")

        return subject, message

    @staticmethod
    def generate_limit_email(user, post_limit, group_name):
        """
        Формирует письмо для уведомления пользователя о превышении лимита постов.

        Аргументы:
        - `user`: Объект пользователя, которому будет отправлено письмо.
        - `post_limit`: Лимит постов, который был достигнут (3 или 5).
        - `group_name`: Название группы пользователя (`basic` или `premium`).
        """
        if group_name == 'basic':
            subject = "Лимит публикаций достигнут"
            message = (
                f"Здравствуй, {user.first_name} {user.last_name}!\n\n"
                f"Вы не можете публиковать более 3 постов в сутки.\n"
                f"Для получения лимита в 5 постов в сутки, перейдите в группу Premium.\n\n"
                f"С уважением,\nКоманда сайта"
            )
        elif group_name == 'premium':
            subject = "Лимит публикаций для Premium-пользователей достигнут"
            message = (
                f"Здравствуй, {user.first_name} {user.last_name}!\n\n"
                f"Как пользователь группы Premium, Вы не можете публиковать более 5 постов в сутки.\n\n"
                f"С уважением,\nКоманда сайта"
            )
        return subject, message

    @staticmethod
    def generate_weekly_digest_email(category, new_articles):
        """
        Создание еженедельного дайджеста новых статей в категории.

        Аргументы:
        - `category`: Категория, по которой генерируется дайджест.
        - `new_articles`: Список новых статей в категории за последнюю неделю.
        """
        # Составляем заголовок письма
        subject = f"Еженедельный дайджест новых статей в категории {category.name}"

        # Формируем содержание письма
        message = f"Здравствуй!\n\nВот список новых статей в категории {category.name} за последнюю неделю:\n\n"

        for article in new_articles:
            message += f"Название: {article.title}\n"
            message += f"Автор: {article.author_profile.user.get_full_name() or article.author_profile.user.username}\n"
            message += f"Краткое содержание: {article.content[:100]}...\n"
            message += f"Прочитать статью: http://127.0.0.1:8000/news/{article.pk}\n\n"

        message += "С уважением,\nКоманда сайта"
        return subject, message



# *************************************************


def send_custom_email(subject, message, recipient_list, use_console_backend=None, html_message=False):
    """
    Вспомогательная функция для отправки email.
    - `subject`: Тема письма.
    - `message`: Сообщение.
    - `recipient_list`: Список email адресов получателей.
    - `use_console_backend`: Переопределяет глобальную настройку использования консольного backend (True/False).
    - `html_message`: Использовать HTML формат сообщения (True/False).
    """
    # Используем глобальную настройку, если параметр use_console_backend не указан
    use_console_backend = settings.USE_CONSOLE_EMAIL_BACKEND if use_console_backend is None else use_console_backend

    # Получаем значение backend для использования
    email_backend = settings.EMAIL_BACKEND_CONSOLE if use_console_backend else settings.EMAIL_BACKEND_SMTP

    # Создаём подключение на основе выбранного backend
    connection = get_connection(backend=email_backend)

    # Отправка письма с использованием реального или консольного backend
    send_mail(
        subject=subject,
        message=message if not html_message else '',  # Если используется HTML, обычное сообщение не отправляется
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=message if html_message else None,
        connection=connection  # Используем тестовый или реальный backend на основе выбора
    )

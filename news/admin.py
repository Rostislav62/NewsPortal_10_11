# Путь: NewsPortal/news/admin.py


from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, Article, Category, Rating

class ProfileAdmin(admin.ModelAdmin):
    """
    Класс админки для отображения расширенной информации о пользователях (Profile).
    """

    # Определяем поля, которые будут отображаться в админке
    list_display = (
        'user_full_name',  # Имя и фамилия
        'user_username',   # Логин
        'user_email',      # Email
        'user_groups',     # Группы, в которых состоит
        'date_joined',     # Дата регистрации
    )

    # Определяем поля, по которым можно искать пользователей
    search_fields = (
        'user__username',  # Поиск по логину
        'user__first_name',  # Поиск по имени
        'user__last_name',   # Поиск по фамилии
        'user__email',       # Поиск по email
    )

    # Определяем фильтры для админки
    list_filter = (
        'user__groups',  # Фильтр по группам
        'user__date_joined',  # Фильтр по дате регистрации
    )

    # Кастомные методы для отображения полей

    def user_full_name(self, obj):
        """
        Возвращает полное имя пользователя (Имя + Фамилия).
        """
        return f"{obj.user.first_name} {obj.user.last_name}"

    def user_username(self, obj):
        """
        Возвращает логин пользователя.
        """
        return obj.user.username

    def user_email(self, obj):
        """
        Возвращает email пользователя.
        """
        return obj.user.email

    def user_groups(self, obj):
        """
        Возвращает группы, в которых состоит пользователь.
        """
        return ", ".join([group.name for group in obj.user.groups.all()])

    def date_joined(self, obj):
        """
        Возвращает дату регистрации пользователя.
        """
        return obj.user.date_joined

    # Настройка отображения названий колонок в админке
    user_full_name.short_description = 'Имя и фамилия'
    user_username.short_description = 'Логин'
    user_email.short_description = 'Email'
    user_groups.short_description = 'Группы'
    date_joined.short_description = 'Дата регистрации'


class ArticleAdmin(admin.ModelAdmin):
    # Создаем кастомные методы для отображения полей
    def author_name(self, obj):
        """
        Возвращает полное имя автора (first_name + last_name).
        """
        return f"{obj.author_profile.user.first_name} {obj.author_profile.user.last_name}"

    def article_type_display(self, obj):
        """
        Возвращает строку "Новость" или "Статья" в зависимости от значения поля article_type.
        """
        return "Новость" if obj.article_type else "Статья"

    def category_name(self, obj):
        """
        Возвращает имя категории, если категория существует.
        """
        return obj.category.name if obj.category else "Категория не указана"

    # Указываем созданные методы в list_display
    list_display = (
        'title',          # Отображение заголовка
        'publication_date',  # Дата публикации
        'author_name',    # Кастомное отображение имени и фамилии автора
        'article_type_display',  # Кастомное отображение типа статьи
        'category_name',   # Кастомное отображение имени категории
        'content' # Содержание поста
    )

    # Добавляем фильтры в админку по полям модели
    list_filter = ('publication_date', 'author_profile', 'category')

    # Добавляем возможность поиска по заголовку и контенту
    search_fields = ('title', 'content')

    # Указываем описание для отображаемых полей в админке
    author_name.short_description = 'Имя автора'  # Переименование колонки
    article_type_display.short_description = 'Тип публикации'  # Переименование колонки
    category_name.short_description = 'Категория'  # Переименование колонки




class CategoryAdmin(admin.ModelAdmin):
    # Исключаем ManyToManyField из отображения в админке
    list_display = [field.name for field in Category._meta.get_fields() if field.many_to_many is False]

    # list_filter и search_fields должны быть кортежами или списками, даже если одно поле
    list_filter = ('name',)  # Используйте поля, которые можно фильтровать
    search_fields = ('name',)  # Обратите внимание на запятую, чтобы это был кортеж


class RatingAdmin(admin.ModelAdmin):
    # Исключаем ManyToManyField из отображения в админке
    list_display = [field.name for field in Rating._meta.get_fields() if field.many_to_many is False]

    # list_filter и search_fields должны быть кортежами или списками, даже если одно поле
    list_filter = ('value',)  # Обратите внимание на запятую, чтобы это был кортеж
    search_fields = ('value',)  # Обратите внимание на запятую, чтобы это был кортеж


# Регистрируем модели в админке с новыми настройками
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Rating, RatingAdmin)

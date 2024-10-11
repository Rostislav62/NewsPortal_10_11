# Путь: <ваше приложение>/management/commands/delete_category_news.py

from django.core.management.base import BaseCommand
from news.models import Article, Category  # Импортируйте модели, которые вы используете


class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории после подтверждения в консоли'

    def add_arguments(self, parser):
        """
        Добавление аргументов командной строки.
        """
        parser.add_argument(
            'category_name',
            type=str,
            help='Название категории, из которой нужно удалить все новости.'
        )

    def handle(self, *args, **kwargs):
        """
        Логика выполнения команды.
        """
        category_name = kwargs['category_name']

        # Получение категории
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Категория с названием '{category_name}' не найдена."))
            return

        # Получение списка новостей в категории
        articles = Article.objects.filter(category=category)

        if not articles.exists():
            self.stdout.write(self.style.WARNING(f"В категории '{category_name}' нет новостей для удаления."))
            return

        # Подтверждение действия перед удалением
        self.stdout.write(self.style.WARNING(
            f"Вы собираетесь удалить все {articles.count()} новостей из категории '{category_name}'."))

        confirm = input(f"Вы уверены, что хотите удалить все новости в категории '{category_name}'? (yes/no): ")

        if confirm.lower() == 'yes':
            # Удаление всех новостей в категории
            articles.delete()
            self.stdout.write(self.style.SUCCESS(f"Все новости из категории '{category_name}' успешно удалены."))
        else:
            self.stdout.write(
                self.style.NOTICE(f"Удаление отменено. Новости в категории '{category_name}' не были удалены."))

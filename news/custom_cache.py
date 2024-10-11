import os
import logging
from django.core.cache.backends.filebased import FileBasedCache

# Инициализация логгера для кастомного кэша
logger = logging.getLogger('news.custom_cache')

class LoggingFileBasedCache(FileBasedCache):
    """
    Пользовательский кэш-бэкэнд, который логирует создание кэша и его привязку к страницам.
    """

    def set(self, key, value, timeout=None, version=None):
        """
        Переопределение метода set для добавления логирования.
        """
        # Вызов оригинального метода set для сохранения кэша
        super().set(key, value, timeout, version)

        # Получаем путь к файлу кэша
        cache_file = self._key_to_file(key)

        # Логируем создание кэш-файла, выводя сообщение в консоль
        if os.path.exists(cache_file):
            logger.info(f"Создан файл кэша: {cache_file} для ключа: {key}")
        else:
            logger.warning(f"Не удалось создать файл кэша для ключа: {key}")

import sqlite3
import json
import base64

# Путь к базе данных SQLite (укажите правильный путь к файлу базы данных)
db_path = r'c:\Users\rsmiglix\OneDrive - Intel Corporation\Documents\GitHub\NewsPortal\db.sqlite3'

# Путь к JSON файлу с данными (укажите правильный путь к вашему JSON файлу)
input_json = 'all_data.json'

# Соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Загружаем данные из JSON файла
with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Вставка данных в каждую таблицу
for table_name, rows in data.items():
    if not rows:
        continue

    # Заключаем имена столбцов в двойные кавычки, чтобы избежать ошибок с зарезервированными словами
    columns = ', '.join([f'"{column}"' for column in rows[0].keys()])
    placeholders = ', '.join(['?'] * len(rows[0]))

    # Изменяем запрос на INSERT OR REPLACE
    insert_query = f'INSERT OR REPLACE INTO "{table_name}" ({columns}) VALUES ({placeholders})'

    # Вставляем каждую строку в таблицу
    for row in rows:
        # Преобразуем обратно поля, которые были закодированы в base64
        for key, value in row.items():
            if isinstance(value, str) and len(value) % 4 == 0:
                try:
                    # Пробуем декодировать значение из base64 обратно в bytes
                    row[key] = base64.b64decode(value.encode('utf-8'))
                except Exception:
                    pass  # Если декодирование не удалось, оставляем значение как есть

        # Выполняем вставку строки в таблицу
        try:
            cursor.execute(insert_query, list(row.values()))
        except sqlite3.IntegrityError as e:
            print(f"Ошибка вставки данных в таблицу {table_name}: {e}")
            continue
        except sqlite3.OperationalError as e:
            print(f"Ошибка синтаксиса при вставке в таблицу {table_name}: {e}")
            continue

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print(f"Данные из {input_json} успешно загружены в базу данных {db_path}.")

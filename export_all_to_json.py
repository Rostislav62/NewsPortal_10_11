import sqlite3
import json
import base64

# Путь к базе данных SQLite
db_path = r'c:\Users\rsmiglix\OneDrive - Intel Corporation\Documents\GitHub\NewsPortal\db.sqlite3'

# Имя выходного JSON файла
output_json = 'all_data.json'

# Соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получение списка всех таблиц в базе данных
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Создаем словарь для хранения данных всех таблиц
data = {}

# Выгружаем все данные из каждой таблицы
for table_name in tables:
    table_name = table_name[0]
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    # Получаем имена столбцов таблицы
    columns = [description[0] for description in cursor.description]
    table_data = []

    # Преобразуем каждую строку
    for row in rows:
        row_dict = {}
        for col_name, col_value in zip(columns, row):
            # Если значение типа bytes, преобразуем его в строку base64 или utf-8
            if isinstance(col_value, bytes):
                row_dict[col_name] = base64.b64encode(col_value).decode('utf-8')  # Преобразование в строку base64
            else:
                row_dict[col_name] = col_value
        table_data.append(row_dict)

    data[table_name] = table_data

# Сохраняем данные в JSON файл
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Данные успешно выгружены в {output_json}")

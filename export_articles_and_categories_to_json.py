import sqlite3
import json
import base64

# Путь к базе данных SQLite
db_path = r'c:\Users\rsmiglix\OneDrive - Intel Corporation\Documents\GitHub\NewsPortal\db.sqlite3'

# Имя выходного JSON файла
output_json = 'articles_and_categories.json'

# Соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Указываем правильные имена таблиц в базе данных
tables = ['news_article', 'news_category']

# Создаем словарь для хранения данных из выбранных таблиц
data = {}

# Выгружаем данные из указанных таблиц
for table_name in tables:
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    # Получаем имена столбцов таблицы
    columns = [description[0] for description in cursor.description]

    table_data = []
    for row in rows:
        row_dict = {}
        for col_name, col_value in zip(columns, row):
            # Если значение столбца является байтовым, преобразуем его в base64
            if isinstance(col_value, bytes):
                row_dict[col_name] = base64.b64encode(col_value).decode('utf-8')
            else:
                row_dict[col_name] = col_value
        table_data.append(row_dict)

    data[table_name] = table_data

# Сохраняем данные в JSON файл
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Данные из таблиц 'news_article' и 'news_category' успешно выгружены в {output_json}")

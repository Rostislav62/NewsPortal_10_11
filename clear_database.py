import sqlite3

# Путь к базе данных SQLite
db_path = r'c:\Users\rsmiglix\OneDrive - Intel Corporation\Documents\GitHub\NewsPortal\db.sqlite3'

# Соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получение списка всех таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = cursor.fetchall()

# Удаление всех записей из каждой таблицы
for table_name in tables:
    table_name = table_name[0]
    cursor.execute(f"DELETE FROM {table_name}")
    print(f"Все данные из таблицы {table_name} удалены.")

# Сохранение изменений
conn.commit()
conn.close()

print("Все данные из базы данных удалены, таблицы остаются пустыми.")

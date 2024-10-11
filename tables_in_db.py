import sqlite3

# Путь к базе данных SQLite
db_path = r'c:\Users\rsmiglix\OneDrive - Intel Corporation\Documents\GitHub\NewsPortal\db.sqlite3'

# Соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Выполнение запроса для получения списка всех таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Вывод имен всех таблиц
print("Существующие таблицы в базе данных:")
for table in tables:
    print(table[0])

conn.close()

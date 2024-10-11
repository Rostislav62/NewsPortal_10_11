import sqlite3

# Путь к базе данных SQLite
db_path = r'c:\Users\rsmiglix\OneDrive - Intel Corporation\Documents\GitHub\NewsPortal\db.sqlite3'

# Соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Очищаем все записи из таблиц перед вставкой
cursor.execute("DELETE FROM news_category;")
cursor.execute("DELETE FROM news_article;")
# Добавьте здесь очистку других таблиц, если необходимо

conn.commit()
conn.close()

print("Все данные из таблиц были удалены перед вставкой.")

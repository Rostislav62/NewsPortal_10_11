import sqlite3
import xml.etree.ElementTree as ET
import base64

# Путь к базе данных SQLite
db_path = r'c:\Users\rsmiglix\OneDrive - Intel Corporation\Documents\GitHub\NewsPortal\db.sqlite3'

# Имя выходного XML файла
output_xml = 'all_data.xml'

# Соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создание корневого элемента XML
root = ET.Element("database")

# Получение списка всех таблиц в базе данных
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Добавление данных каждой таблицы в XML
for table_name in tables:
    table_name = table_name[0]
    table_element = ET.SubElement(root, table_name)

    # Выполнение запроса и получение данных таблицы
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    # Добавление каждой строки таблицы в XML
    for row in rows:
        row_element = ET.SubElement(table_element, "row")
        for col_name, col_value in zip(columns, row):
            col_element = ET.SubElement(row_element, col_name)

            # Если значение столбца является байтовым, преобразуем его в base64
            if isinstance(col_value, bytes):
                col_element.text = base64.b64encode(col_value).decode('utf-8')
                col_element.set("type", "base64")  # Добавляем атрибут type для указания, что это base64
            else:
                col_element.text = str(col_value)

# Создание объекта дерева и запись в файл
tree = ET.ElementTree(root)
tree.write(output_xml, encoding='utf-8', xml_declaration=True)

print(f"Данные успешно выгружены в {output_xml}")

# Шаблон для 1 таблицы (category.csv)
import csv
import sqlite3

conn= sqlite3.connect("db.sqlite3")
c = conn.cursor()

with open("static/data/category.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            "INSERT INTO reviews_category "
            "(id, name, slug) "
            "VALUES(?, ?, ?)",
            (id, name, slug)
        )
        conn.commit()

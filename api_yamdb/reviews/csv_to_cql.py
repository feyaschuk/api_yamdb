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

with open("static/data/comments.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        review_id = row['review_id']
        text = row['text']
        author = row['author']
        pub_date = row['pub_date']
        c.execute(
            "INSERT INTO reviews_comments "
            "(id, review_id, text, author, pub_date) "
            "VALUES(?, ?, ?, ?, ?)",
            (id, review_id, text, author, pub_date)
        )
        conn.commit()

with open("static/data/genre.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            "INSERT INTO reviews_genre "
            "(id, name, slug) "
            "VALUES(?, ?, ?)",
            (id, name, slug)
        )
        conn.commit()

with open("static/data/genre_title.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        title_id = row['title_id']
        genre_id = row['genre_id']
        c.execute(
            "INSERT INTO reviews_genre_title "
            "(id, title_id, genre_id) "
            "VALUES(?, ?, ?)",
            (id, title_id, genre_id)
        )
        conn.commit()

with open("static/data/review.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        title_id = row['title_id']
        text = row['text']
        title_id = row['author']
        text = row['score']
        title_id = row['title_id']
        text = row['pub_date']
        c.execute(
            "INSERT INTO reviews_review "
            "(id, title_id, text, author, score, pub_date) "
            "VALUES(?, ?, ?, ?, ?, ?)",
            (id, title_id, text, author, score, pub_date)
        )
        conn.commit()

with open("static/data/titles.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        year = row['year']
        category = row['category']
        c.execute(
            "INSERT INTO reviews_titles "
            "(id, name, year, category) "
            "VALUES(?, ?, ?, ?)",
            (id, name, year, category)
        )
        conn.commit()

with open("static/data/users.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        username = row['username']
        email = row['email']
        role = row['role']
        bio = row['bio']
        first_name = row['first_name']
        last_name = row['last_name']
        c.execute(
            "INSERT INTO reviews_users "
            "(id, username, email, role, bio, first_name, last_name) "
            "VALUES(?, ?, ?, ?, ?, ?, ?)",
            (id, username, email, role, bio, first_name, last_name)
        )
        conn.commit()
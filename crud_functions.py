import sqlite3

connection = sqlite3.connect('initiate.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
)
""")
# for i in range(1, 5):
#     cursor.execute('INSERT INTO Products (title, description, price) VALUES (?,?,?)', (f"Продукт {i}",f"Описание {i}",f"Цена {i * 100}"))

# cursor.execute("""DELETE FROM Users""")


def get_all_products():
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products

def get_title_products():
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM Products")
    title = cursor.fetchall()
    connection.commit()
    connection.close()
    return title

def add_user(username, email, age):
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE username = ?)", (username,))
    exists = cursor.fetchone()[0]
    connection.close()
    return bool(exists)

connection.commit()
connection.close()
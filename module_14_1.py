import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
""")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users(email)')
cursor.execute("DELETE FROM Users;") # удаление данных из таблицы(для проверки УДАЛИТЬ!!)
for i in range(1,11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)', (f"User{i}",f"example{i}@gmail.com",f"{i}0", "1000"))
cursor.execute("UPDATE Users SET balance = balance - 500 WHERE id % 2 = 1") # Обновите balance у каждой 2ой записи начиная с 1ой на 500:
cursor.execute("DELETE FROM Users WHERE id % 3 = 1") # Удалите каждую 3ую запись в таблице начиная с 1ой:
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")#
results = cursor.fetchall()
for row in results:
    username, email, age, balance = row
    print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')
connection.commit()
connection.close()

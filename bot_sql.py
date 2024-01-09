import sqlite3


class SqlBot:
    def __init__(self):
        self.connect = sqlite3.connect('bot_sql.db')
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            price INTEGER,
            product TEXT,
            count INTEGER,
            link TEXT);
            '''
        )

    def add_users(self, user_id, product, price, count, link):
        self.cursor.execute(
            'INSERT INTO users (user_id, product, price, count, link) VALUES (?, ?, ?, ?, ?)',
            (user_id, product, price, count, link)
        )
        self.connect.commit()


sql = SqlBot()
sql.create_table()

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
            article INTEGER,
            price INTEGER,
            product TEXT,
            count INTEGER,
            link TEXT);
            '''
        )

    def add_users(self, user_id, article, product, price, count, link):
        '''Добавить данные в базу'''

        self.cursor.execute("SELECT id FROM users WHERE user_id = ? AND article = ?", (user_id, article))
        existing_product = self.cursor.fetchone()

        if not existing_product:
            # Если товар с такой ценой не существует, то добавляем товар в базу данных
            self.cursor.execute(
                'INSERT INTO users (user_id, article, product, price, count, link) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, article, product, price, count, link)
            )
            self.connect.commit()

    def look_link(self, user_id):
        self.cursor.execute("SELECT * FROM users;")
        return [i[-1] for i in self.cursor.fetchall() if user_id in i]

    def look_product_none_price(self, user_id):
        self.cursor.execute("SELECT * FROM users;")
        return [i[2:5:2] for i in self.cursor.fetchall() if user_id in i]

    def look_product(self, user_id):
        self.cursor.execute("SELECT * FROM users;")
        return [i[2::] for i in self.cursor.fetchall() if user_id in i]

    def del_data(self):
        '''Удалить данные пользователя'''
        ...


sql = SqlBot()
# sql.create_table()
print(sql.look_product(514132114))

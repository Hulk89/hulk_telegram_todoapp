import sqlite3


class DBHelper:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt = """CREATE TABLE IF NOT EXISTS items (description CHAR(100),
                                                    telegramid   INT )"""

        self.conn.execute(stmt)
        self.conn.commit()
        

    def add_item(self, item_text, telegram_id):
        stmt = "INSERT INTO items (description, telegramid) VALUES (?, ?)"
        args = (item_text, telegram_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, telegram_id):
        stmt = "DELETE FROM items WHERE description = ? AND telegramid = ?"
        args = (item_text, telegram_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, telegram_id):
        stmt = "SELECT description FROM items WHERE telegramid = ?"
        args = (telegram_id, )
        return [x[0] for x in self.conn.execute(stmt, args)]


if __name__ == '__main__':
    helper = DBHelper(dbname="test.sqlite")
    helper.setup()
    helper.add_item("test", 33)
    res = helper.get_items(33)
    print(res)
    helper.delete_item("test", 33)
    res = helper.get_items(33)
    print(res)
    
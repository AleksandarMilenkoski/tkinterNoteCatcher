import sqlite3 as lite


class TableAbstract:
    """docstring for TableAbstract"""

    def __init__(self, path):
        self.connection = lite.connect(path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()


if __name__ == '__main__':
    TableAbstract('../../db.db')

import sqlite3 as lite


class TableAbstract:
    """docstring for TableAbstract"""

    def __init__(self):
        self.connection = lite.connect('../../db.db')
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

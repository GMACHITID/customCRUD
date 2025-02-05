import psycopg2
from config import DB_CONFIG

class DatabaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            DB_CONFIG
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

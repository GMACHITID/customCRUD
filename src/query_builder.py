from src.db import DatabaseConnection

class QueryBuilder:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def insert_one(self, table_name, columns, values):
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});"
        self.db.cursor.execute(query, values)
        self.db.conn.commit()

    def fetch_all(self, table_name):
        query = f"SELECT * FROM {table_name};"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def fetch_with_condition(self, table_name, condition):
        query = f"SELECT * FROM {table_name} WHERE {condition};"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

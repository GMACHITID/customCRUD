from src.db import DatabaseConnection

class SchemaManager:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create_table(self, table_name, columns):
        """
        Creates a table in the database.
        :param table_name: Name of the table
        :param columns: Dictionary {column_name: column_type}
        """
        column_definitions = ", ".join(f"{col} {dtype}" for col, dtype in columns.items())
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"

        self.db.cursor.execute(query)
        self.db.conn.commit()

    def add_column(self, table_name, column_name, data_type):
        query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};"
        self.db.cursor.execute(query)
        self.db.conn.commit()

    def drop_column(self, table_name, column_name):
        query = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
        self.db.cursor.execute(query)
        self.db.conn.commit()

    def modify_column_type(self, table_name, column_name, new_data_type):
        """Modify the data type of an existing column."""
        query = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_data_type};"
        self.db.cursor.execute(query)
        self.db.conn.commit()

    def rename_column(self, table_name, old_name, new_name):
        """Rename a column."""
        query = f"ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name};"
        self.db.cursor.execute(query)
        self.db.conn.commit()

    def rename_table(self, old_name, new_name):
        """Rename a table."""
        query = f"ALTER TABLE {old_name} RENAME TO {new_name};"
        self.db.cursor.execute(query)
        self.db.conn.commit()

    def drop_table(self, table_name):
        """Drop a table from the database."""
        query = f"DROP TABLE IF EXISTS {table_name};"
        self.db.cursor.execute(query)
        self.db.conn.commit()

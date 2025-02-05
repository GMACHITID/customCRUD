from src.db import DatabaseConnection

class BaseModel:
    """Base ORM model with common database operations."""

    db = None  # Will be set when models are initialized

    def __init__(self, **kwargs):
        """Initialize model instance with given attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def set_db(cls, db: DatabaseConnection):
        """Attach a database connection to the BaseModel."""
        cls.db = db

    @classmethod
    def create(cls, **kwargs):
        """Insert a new record into the database."""
        table_name = cls.__name__.lower()
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s'] * len(kwargs))
        values = tuple(kwargs.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING *;"
        cls.db.cursor.execute(query, values)
        cls.db.conn.commit()
        return cls(**cls.db.cursor.fetchone())

    @classmethod
    def get_all(cls):
        """Fetch all records from the table."""
        table_name = cls.__name__.lower()
        query = f"SELECT * FROM {table_name};"
        cls.db.cursor.execute(query)
        rows = cls.db.cursor.fetchall()
        results = []
        columns = [col[0] for col in cls.db.cursor.description]  # Extract column names

        for row in rows:
            data_dict = dict(zip(columns, row))  # Pair column names with row values
            results.append(cls(**data_dict))  # Convert to object

        return results

    @classmethod
    def filter(cls, **conditions):
        """Fetch records based on filter conditions."""
        table_name = cls.__name__.lower()
        where_clause = ' AND '.join([f"{key} = %s" for key in conditions.keys()])
        values = tuple(conditions.values())

        query = f"SELECT * FROM {table_name} WHERE {where_clause};"
        cls.db.cursor.execute(query, values)
        rows = cls.db.cursor.fetchall()
        results = []
        columns = [col[0] for col in cls.db.cursor.description]  # Extract column names

        for row in rows:
            data_dict = dict(zip(columns, row))  # Pair column names with row values
            results.append(cls(**data_dict))  # Convert to object

        return results

    def update(self, **kwargs):
        """Update an existing record in the database."""
        table_name = self.__class__.__name__.lower()
        set_clause = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        values = tuple(kwargs.values()) + (getattr(self, 'id'),)

        query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s RETURNING *;"
        self.db.cursor.execute(query, values)
        self.db.conn.commit()

        updated_row = self.db.cursor.fetchone()
        for key, value in zip([col[0] for col in self.db.cursor.description], updated_row):
            setattr(self, key, value)

    def delete(self):
        # Identify the primary key column dynamically
        table_name = self.__class__.__name__.lower()
        columns = [col[0] for col in self.db.cursor.description]  # Extract column names

        # Assume the first column is the primary key
        primary_key = columns[0] if columns else "id"

        # Get the primary key value from the instance
        primary_key_value = getattr(self, primary_key, None)

        if primary_key_value is None:
            raise ValueError(f"Cannot delete {table_name} because no primary key value is set.")

        query = f"DELETE FROM {table_name} WHERE {primary_key} = %s RETURNING {primary_key};"
        self.db.cursor.execute(query, (primary_key_value,))
        deleted_id = self.db.cursor.fetchone()

        self.db.conn.commit()

        return deleted_id is not None  # Return True if deletion was successful

from src.schema_manager import SchemaManager
from src.db import DatabaseConnection

db = DatabaseConnection()

# Initialize schema manager
schema_manager = SchemaManager(db)

# Create tables for User and Product
# Define table structure
user_table_columns = {
    "id": "SERIAL PRIMARY KEY",
    "name": "VARCHAR(255) NOT NULL",
    "email": "VARCHAR(255) UNIQUE",
    "age": "INT"
}

# Create the table
schema_manager.create_table("users", user_table_columns)

db.cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users');")
assert db.cursor.fetchone()[0], "Table 'users' was NOT created!"


print("Table created successfully!")
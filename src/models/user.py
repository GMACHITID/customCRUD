from src.base_model import BaseModel

class User(BaseModel):
    table_name = "users"
    columns = ["id", "name", "email", "created_at"]

    def __init__(self, name, email, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.email = email

    def save(self):
        return self.create(
            table_name=self.table_name,
            columns=["name", "email"],
            values=[self.name, self.email]
        )

from src.base_model import BaseModel

class Product(BaseModel):
    table_name = "products"
    columns = ["id", "name", "price", "description", "created_at"]

    def __init__(self, name, price, description=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.price = price
        self.description = description

    def save(self):
        return self.create(
            table_name=self.table_name,
            columns=["name", "price", "description"],
            values=[self.name, self.price, self.description]
        )

from .app_factory import db

class Product(db.Model):
    __tablename__ = 'products'
# tablename = название таблицы в sql

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.name} ({self.price} rub.)>'

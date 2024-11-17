from my_app.app_factory import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
# создание таблицы в sql

    id = db.Column(db.Integer, primary_key=True)#id
    name = db.Column(db.String(80), nullable=False)#имя позиции
    price = db.Column(db.Float, nullable=False) #цена
    created_at = db.Column(db.DateTime, default=datetime.utcnow) #время

    def __repr__(self):
        return f'<Product {self.name} ({self.price} rub.)>'

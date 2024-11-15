from my_app.app_factory import db

class Product(db.Model):
    __tablename__ = 'products'
# создание таблицы в sql

    id = db.Column(db.Integer, primary_key=True)#id
    name = db.Column(db.String(80), nullable=False)#имя позиции
    description = db.Column(db.String(200), nullable=True) #описание
    price = db.Column(db.Float, nullable=False) #цена

    def __repr__(self):
        return f'<Product {self.name} ({self.price} rub.)>'

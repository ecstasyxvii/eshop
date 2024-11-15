from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# инициализация фабрики приложения 
# (вместо того чтобы создавать глобальный объект приложения app сразу при запуске программы, 
# мы используем класс и функцию который создает и настраивает приложение только тогда когда это нужно)

class AppFactory:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.app = None

    #создание приложения 
    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #инициализация базы данных
        db.init_app(self.app) 
        global migrate
        migrate = Migrate(self.app, db)

        from .models import Product

        self.register_routes()
        return self.app
    

    # регистрация маршрутов(ссылок) 
    def register_routes(self):
        from .models import Product

#db.session.commit() - сохранение в бд
#db.session.add(product) - добавление обьекта в миграцию

        #возврат всех товаров находящихся в дб
        @self.app.route('/products/<int:product_id>', methods=['GET']) 
        def get_product(product_id): 
            product = Product.query.get(product_id) #получение данных из таблицы products по id товара

            if not product:
                return jsonify({"error": "Product not found"}), 404

            return jsonify([{
                "id":product.id,
                "name":product.name,  
                "price":product.price
            }]) #перевожу обьекты в json
        
        #добавление товара
        @self.app.route('/products', methods=['POST'])
        def add_product():
            data = request.get_json()

            #проверка данных
            if not data or not data.get('name') or not data.get('price'):
                return jsonify({"error": "Invalid input"}), 400

            #создание товара
            product = Product(name=data['name'], price=data['price'])
            db.session.add(product) 
            db.session.commit()

            return jsonify({"message": "Product added", "id": product.id}), 201 
        
        #обновление информации о товаре
        @self.app.route('/products/<int:product_id>', methods=['PUT'])
        def update_product(product_id):
            data = request.get_json()
            product = Product.query.get(product_id)

            if not product:
                return jsonify({"error": "Product not found"}), 404
            
            #обновление данных
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            db.session.commit()

            return jsonify({"message": "Product updated"})

        #удаление товара
        @self.app.route('/products/<int:product_id>', methods=['DELETE'])
        def delete_product(product_id):
            product = Product.query.get(product_id)

            if not product:
                return jsonify({"error": "Product not found"}), 404
            
            db.session.delete(product)
            db.session.commit()

            return jsonify({"message": "Product deleted"})
        
        #поиск товара по диапазону цен и имени
        @self.app.route('/products/search', methods=['GET'])
        def search_products():
            name = request.args.get('name', '')
            min_price = request.args.get('min_price', type=float)
            max_price = request.args.get('max_price', type=float)

            query = Product.query

            if name:
                query = query.filter(Product.name.ilike(f'%{name}%'))
            if min_price is not None:
                query = query.filter(Product.price >= min_price)
            if max_price is not None:
                query = query.filter(Product.price <= max_price)

            products = query.all()

            return jsonify([{
                "id":p.id,
                "name":p.name,
                "price":p.price
            } for p in products])
        
        @self.app.route('/products/html', methods=['GET'])
        def show_products():
            products = Product.query.all()
            return render_template('products.html', products=products)
        
        #обработка ошиби 404 и 400 
        @self.app.errorhandler(404)
        def not_found_error(error):
            return jsonify({"error": "Not found"}), 404
        
        @self.app.errorhandler(400)
        def bad_request_error(error):
            return jsonify({"error": "Bad request"}), 400

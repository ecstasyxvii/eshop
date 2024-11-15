from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

class AppFactory:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.app = None

    # инициализация фабрики приложения 
    # (вместо того чтобы создавать глобальный объект приложения app сразу при запуске программы, 
    # мы используем класс и функцию который создает и настраивает приложение только тогда когда это нужно)

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        

        db.init_app(self.app)  #инициализация базы данных
        global migrate
        migrate = Migrate(self.app, db)

        from .models import Product

        self.register_routes()
        return self.app
    

    # регистрация маршрутов(ссылок) 
    def register_routes(self):
        @self.app.route('/')
        def home():
            return 'lmao'

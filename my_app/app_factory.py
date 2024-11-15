from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# определение базы данных
db = SQLAlchemy()

class AppFactory:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.app = None
        self.migrate = None

    # инициализация фабрики приложения 
    # Фабрика приложения — это специальный подход к созданию Flask-приложений. 
    # Вместо того чтобы создавать глобальный объект приложения app сразу при запуске программы, 
    # мы используем функцию или класс, которые создают и настраивают приложение только тогда, когда это нужно.

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)  # Инициализируем базу данных
        self.migrate = Migrate(self.app, db)
        self.register_routes()
        return self.app
    
    # регистрация маршрутов(ссылок) 
    def register_routes(self):
        @self.app.route('/')
        def home():
            return 'lmao'
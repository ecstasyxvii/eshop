from my_app.app_factory import AppFactory

factory = AppFactory('postgresql://postgres:admin@localhost:5432/eshop')
app = factory.create_app()

if __name__ == '__main__':
    app.run(debug=True)
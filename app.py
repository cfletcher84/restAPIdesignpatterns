from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from database import db
from schemas import ma
from limiter import limiter

from models.customer import Customer
from models.employee import Employee
from models.order import Order
from models.production import Production
from models.product import Product

from routes.customerBP import customer_blueprint
from routes.employeeBP import employee_blueprint
from routes.orderBP import order_blueprint
from routes.productBP import product_blueprint
from routes.productionBP import production_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(

SWAGGER_URL,
API_URL,
config={'app_name': 'CT E-Commerce'}
)



def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)

    return app

def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(employee_blueprint, url_prefix='/employees')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(production_blueprint, url_prefix='/production')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def config_rate_limit():
    limiter.limit("100 per day")(customer_blueprint)
    limiter.limit("100 per day")(employee_blueprint)
    limiter.limit("100 per day")(order_blueprint)
    limiter.limit("100 per day")(product_blueprint)
    limiter.limit("100 per day")(production_blueprint)

if __name__ == "__main__":
    app = create_app('DevelopmentConfig')

    blueprint_config(app)
    config_rate_limit()

    app.run(debug=True)

from flask import Blueprint
from controllers.customerController import save, find_all

customer_blueprint = Blueprint('customer_bp', __name__)

def placeholder(customer_id):
    return 'Get customer ' + str(customer_id)

customer_blueprint.route('/', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)
customer_blueprint.route('/<customer_id>', methods=['GET]'])
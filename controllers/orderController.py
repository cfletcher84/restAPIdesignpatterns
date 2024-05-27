from flask import request, jsonify
from schemas.orderSchema import order_schema, orders_schema
from services import orderServices
from marshmallow import ValidationError

def save():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    order_save = orderServices.save(order_data)
    return order_schema.jsonify(order_save), 201

def find_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    orders = orderServices.find_all(page, per_page)
    return orders_schema.jsonify(orders)
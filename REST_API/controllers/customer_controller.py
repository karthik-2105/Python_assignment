from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService

customer_bp = Blueprint('customer_bp', __name__)
service = CustomerService()

@customer_bp.route('/', methods=['POST'])
def add_customer():
    data = request.get_json()
    return jsonify(service.insert_customer(data)), 201

@customer_bp.route('/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return jsonify(service.get_customer(customer_id)), 200

@customer_bp.route('/<string:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    return jsonify(service.update_customer(customer_id, data)), 200


@customer_bp.route('/<string:customer_id>/orders', methods=['GET'])
def get_order_history(customer_id):
    orders = service.get_customer_orders(customer_id)
    return jsonify(orders), 200

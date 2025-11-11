from flask import Blueprint, request, jsonify
from services.order_service import OrderService

order_bp = Blueprint('order_bp', __name__)
service = OrderService()

@order_bp.route('/', methods=['POST'])
def add_order():
    data = request.get_json()
    return jsonify(service.insert_order(data)), 201

@order_bp.route('/<string:order_id>', methods=['GET'])
def get_order(order_id):
    return jsonify(service.get_order(order_id)), 200

@order_bp.route('/<string:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    return jsonify(service.update_order(order_id, data)), 200

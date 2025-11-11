from flask import Blueprint, request, jsonify
from services.product_service import ProductService

product_bp = Blueprint('product_bp', __name__)
service = ProductService()

@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    return jsonify(service.insert_product(data)), 201

@product_bp.route('/<string:product_id>', methods=['GET'])
def get_product(product_id):
    return jsonify(service.get_product(product_id)), 200

@product_bp.route('/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    return jsonify(service.update_product(product_id, data)), 200

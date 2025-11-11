from models.product import Product
from utils.db import db

class ProductService:
    def insert_product(self, data):
        # Create a new Product instance
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        return {"message": "Product added successfully"}

    def get_product(self, product_id):
        # Fetch a single product by ID
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found"}
        return {
            "ProductID": product.ProductID,
            "ProductName": product.ProductName,
            "SupplierID": product.SupplierID,
            "CategoryID": product.CategoryID,
            "Unit": product.Unit,
            "Price": product.Price

        }

    def update_product(self, product_id, data):
        # Update an existing product
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found"}
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return {"message": "Product updated successfully"}

    def delete_product(self, product_id):
        # Delete a product
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found"}
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}

        new_customer = Customer(**data)
        db.session.add(new_customer)
        db.session.commit()
        return {"message": "Customer added successfully"}

    
from models.orders import Orders
from utils.db import db

class OrderService:
    def insert_order(self, data):
        # Create a new Order instance
        new_order = Orders(**data)
        db.session.add(new_order)
        db.session.commit()
        return {"message": "Order added successfully"}

    def get_order(self, order_id):
        # Fetch a single order by ID
        order = Orders.query.get(order_id)
        if not order:
            return {"message": "Order  not found"}
        return {
            "OrderID": order.OrderID,
            "CustomerID": order.CustomerID,
            "EmployeeID": order.EmployeeID,
            "OrderDate": str(order.OrderDate),
            "ShipperID": order.ShipperID
            
        }

    def update_order(self, order_id, data):
        # Update an existing order
        order = Orders.query.get(order_id)
        if not order:
            return {"message": "Order not found"}
        for key, value in data.items():
            setattr(order, key, value)
        db.session.commit()
        return {"message": "Order updated successfully"}

    
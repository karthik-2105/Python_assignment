from models.customer import Customer
from utils.db import db

class CustomerService:
    def insert_customer(self, data):
        # Create a new Customer instance
        new_customer = Customer(**data)
        db.session.add(new_customer)
        db.session.commit()
        return {"message": "Customer added successfully"}

    def get_customer(self, customer_id):
        # Fetch a single customer by ID
        customer = Customer.query.get(customer_id)
        if not customer:
            return {"message": "Customer not found"}
        return {
            "CustomerID": customer.CustomerID,
            "CustomerName": customer.CustomerName,
            "Address": customer.Address,
            "City": customer.City,
            "Country": customer.Country

           
        }

    def update_customer(self, customer_id, data):
        # Update an existing customer
        customer = Customer.query.get(customer_id)
        if not customer:
            return {"message": "Customer not found"}
        for key, value in data.items():
            setattr(customer, key, value)
        db.session.commit()
        return {"message": "Customer updated successfully"}

    
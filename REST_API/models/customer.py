from utils.db import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    CustomerID = db.Column(db.String(10), primary_key=True)
    CustomerName = db.Column(db.String(50))
    Address = db.Column(db.String(100))
    City = db.Column(db.String(50))
    Country = db.Column(db.String(50))


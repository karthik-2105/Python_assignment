from utils.db import db

class Orders(db.Model):
    __tablename__ = 'orders'
    
    OrderID = db.Column(db.String(10), primary_key=True)
    CustomerID = db.Column(db.String(10), db.ForeignKey('customers.CustomerID'))
    EmployeeID = db.Column(db.String(10))
    OrderDate = db.Column(db.Date)
    ShipperID = db.Column(db.String(50))


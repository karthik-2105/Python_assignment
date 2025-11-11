from utils.db import db

class Product(db.Model):
    __tablename__ = 'products'

    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(50))
    SupplierID = db.Column(db.Integer)
    CategoryID = db.Column(db.Integer)
    Unit = db.Column(db.String(50))
    Price = db.Column(db.Float)
    

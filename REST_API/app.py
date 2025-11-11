from flask import Flask
from config import Config
from utils.db import db
from controllers.customer_controller import customer_bp
from controllers.product_controller import product_bp
from controllers.order_controller import order_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Register blueprints
app.register_blueprint(customer_bp, url_prefix='/api/customers')
app.register_blueprint(product_bp, url_prefix='/api/products')
app.register_blueprint(order_bp, url_prefix='/api/orders')

if __name__ == '__main__':
    app.run(debug=True)

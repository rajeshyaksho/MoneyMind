#Backend: Flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db, bcrypt
from routes.auth_routes import auth_routes
from routes.transaction_routes import transaction_routes

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)    
jwt = JWTManager(app)
CORS(app)

# Register Blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(transaction_routes, url_prefix='/transactions')

@app.route('/')
def home():
    return "Welcome to the MoneyMind API!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
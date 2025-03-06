from flask import Flask
from flask_cors import CORS
from models.user_model import db
from api.auth_routes import auth_bp
from flask_mail import Mail
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize database
db.init_app(app)

# Initialize mail service
mail = Mail(app)

# Register Blueprint
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Create tables if they don’t exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

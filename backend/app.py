from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db  # ✅ Import the globally shared 'db' instance
from models.user_model import User
from api.auth_routes import auth_bp
from flask_mail import Mail
from utils.email_service import mail
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database and Flask-Mail
db.init_app(app)  # ✅ Ensure SQLAlchemy is correctly linked with Flask

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change this to your email provider's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pensionmanagementtool@gmail.com'  # Change this to your email
app.config['MAIL_PASSWORD'] = 'cnbt kkmb lcvh vczy'  # Use App Password if using Gmail
app.config['MAIL_DEFAULT_SENDER'] = 'pensionmanagementtool@gmail.com'

mail.init_app(app)

# Enable CORS
CORS(app)

# Register authentication routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Serve QR codes via Flask
@app.route('/qrcodes/<filename>')
def serve_qr_code(filename):
    return send_from_directory(os.path.join(os.getcwd(), "backend", "qrcodes"), filename)

# Create database tables before running
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

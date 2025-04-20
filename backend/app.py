from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db  # ✅ Import the globally shared 'db' instance
from models.user_model import User
from models.pension_statement_model import PensionStatement
from api.auth_routes import auth_bp
from api.admin_routes import admin_bp
from flask_mail import Mail
from utils.email_service import mail
import os
from flask_migrate import Migrate
from models.employer_model import Employer 
from models.admin_model import Admin  # ✅ This ensures it gets registered with Flask-Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from tasks.scheduler_tasks import generate_monthly_statements
from api.employer_routes import employer_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database and Flask-Mail
db.init_app(app)  # ✅ Ensure SQLAlchemy is correctly linked with Flask
migrate = Migrate(app, db)

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
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(employer_bp, url_prefix='/api')

# Serve QR codes via Flask
@app.route('/qrcodes/<filename>')
def serve_qr_code(filename):
    return send_from_directory(os.path.join(os.getcwd(), "backend", "qrcodes"), filename)

# Create database tables before running
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

scheduler = BackgroundScheduler()
scheduler.add_job(func=generate_monthly_statements, trigger='interval', days=30)
scheduler.start()

# Ensure shutdown on exit
import atexit
atexit.register(lambda: scheduler.shutdown())
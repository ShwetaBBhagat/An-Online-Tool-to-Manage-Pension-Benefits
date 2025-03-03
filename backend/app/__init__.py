from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load Configurations
    app.config.from_object("app.config.Config")
    
    # Initialize Extensions
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
    
    # Import and Register Routes
    from app.routes import main
    app.register_blueprint(main)

    return app

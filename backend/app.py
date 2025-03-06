from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# Load configurations from config.py
app.config.from_object('config.Config')

# Enable CORS (Cross-Origin Resource Sharing)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize database
db = SQLAlchemy(app)

# Import routes after initializing db to avoid circular import
from routes import *

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

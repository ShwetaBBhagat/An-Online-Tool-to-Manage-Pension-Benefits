from flask import Blueprint, jsonify
from app import db
from sqlalchemy.sql import text
from sqlalchemy import inspect

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message": "Welcome to Pension Management API"})

@main.route("/health")
def health_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "OK", "message": "Database connected successfully!"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
    
@main.route("/list-tables")
def list_tables():
    try:
        inspector = inspect(db.engine)  # Use the new method
        tables = inspector.get_table_names()
        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
    
@main.route("/test-connection")
def test_connection():
    return jsonify({"message": "Angular successfully connected to Flask!"})

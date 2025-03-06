from flask import Flask, jsonify
from app import app

@app.route("/")
def home():
    return jsonify({"message": "Flask backend is running!"})

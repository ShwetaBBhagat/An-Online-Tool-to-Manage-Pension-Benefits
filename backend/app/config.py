import os

class Config:
    # MySQL Database Configuration
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Shweta!17@localhost/pension_management"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security Key
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")

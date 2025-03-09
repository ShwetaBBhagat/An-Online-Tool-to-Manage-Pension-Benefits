import os

class Config:
    SECRET_KEY = "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Shweta!17@localhost/pension_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "pensionmanagementtool@gmail.com"
    MAIL_PASSWORD = "Shweta17@"
   
    # JWT Secret Key
    JWT_SECRET_KEY = "280303"  
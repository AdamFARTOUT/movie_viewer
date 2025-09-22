import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_me")  
    DATABASE = os.environ.get("DATABASE", "users.db")
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "b1f902a3")  # mettre ta clé OMDB ici ou dans .env
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

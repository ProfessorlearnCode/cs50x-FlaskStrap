import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.urandom(24)  # Generate a random secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'  # Use filesystem for session storage
    SESSION_COOKIE_SECURE = True  # Use secure cookies
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # Session lifetime

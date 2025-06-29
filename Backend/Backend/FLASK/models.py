from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    city = db.Column(db.String(180))
    role = db.Column(db.String(10))



def __repr__(self):
    return f'<User {self.username}>'
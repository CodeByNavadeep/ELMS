from extensions import db  
from flask_login import UserMixin

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(100), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')  # New: Pending, Approved, Rejected
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to employee
    user = db.relationship('User', backref='leaves')  # Create relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    #email=db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Employee, Manager, Admin
    

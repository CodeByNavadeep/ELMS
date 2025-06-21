from app import app
from extensions import db
from models import Leave, User

with app.app_context():
    db.drop_all()  # Optional: to ensure clean slate
    db.create_all()
    print("Database created!")

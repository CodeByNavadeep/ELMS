from app import app
from extensions import db
from models import Leave, User

with app.app_context():
    db.create_all()
    print("Database created!")

from dotenv import load_dotenv

load_dotenv()
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():

    admin = User.query.filter_by(email="admin@auranova.com").first()

    if admin:
        print("Admin already exists!")
    else:
        admin = User(
            full_name="System Administrator",
            email="admin@auranova.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")
from getpass import getpass
from backend.app.db import SessionLocal
from backend.app.models.admin import Admin
from backend.app.core.security import hash_password

def main():
    username = input("Admin username: ").strip()
    password = getpass("Admin password: ")
    confirm = getpass("Confirm password: ")

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    if password != confirm:
        print("Passwords do not match.")
        return

    db = SessionLocal()
    try:
        existing = db.query(Admin).filter_by(username=username).first()
        if existing:
            print("Username already exists.")
            return

        admin = Admin(
            username=username,
            password_hash=hash_password(password),
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("Admin account created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    main()

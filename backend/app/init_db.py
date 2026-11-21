from backend.app.db import engine
from backend.app.models import Base

def initialize_database():
    Base.metadata.create_all(bind=engine)
    print("JK Pulse database tables created successfully.")

if __name__ == "__main__":
    initialize_database()

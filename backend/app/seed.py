from backend.app.db import SessionLocal
from backend.app.models.category import Category

categories = [
    ("Jobs & Recruitment", "jobs-recruitment"),
    ("Education", "education"),
    ("Admissions", "admissions"),
    ("Results", "results"),
    ("Admit Cards", "admit-cards"),
    ("Scholarships", "scholarships"),
    ("Exam Preparation", "exam-preparation"),
    ("Current Affairs", "current-affairs"),
    ("News & Updates", "news-updates"),
    ("Datesheets & Syllabus", "datesheets-syllabus"),
    ("Career & Technology", "career-technology"),
]

db = SessionLocal()

try:
    for name, slug in categories:
        existing = db.query(Category).filter_by(slug=slug).first()
        if not existing:
            db.add(Category(name=name, slug=slug))

    db.commit()
    print("JK Pulse categories seeded successfully.")
except Exception as e:
    db.rollback()
    print("Error:", e)
finally:
    db.close()

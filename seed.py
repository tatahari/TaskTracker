from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from datetime import datetime, timedelta

def seed_data():
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(models.Task).count() > 0:
        print("Data already exists, skipping seeding.")
        db.close()
        return

    sample_tasks = [
        {
            "name": "Design Homepage",
            "status": models.TaskStatus.COMPLETED,
            "customer_name": "Acme Corp",
            "stakeholders": "John Doe, Sarah Smith",
            "useful_links": "https://figma.com/design/123",
            "comments": "Initial design approved by client.",
            "due_date": datetime.utcnow() - timedelta(days=2)
        },
        {
            "name": "Develop API",
            "status": models.TaskStatus.IN_PROGRESS,
            "customer_name": "TechStart Inc",
            "stakeholders": "Jane Miller",
            "useful_links": "https://github.com/techstart/api",
            "comments": "Working on authentication endpoints.",
            "due_date": datetime.utcnow() + timedelta(days=5)
        },
        {
            "name": "Setup Database",
            "status": models.TaskStatus.PENDING,
            "customer_name": "Global Logistics",
            "stakeholders": "Mike Ross",
            "useful_links": "https://docs.postgresql.org",
            "comments": "Need to decide between PostgreSQL and MySQL.",
            "due_date": datetime.utcnow() + timedelta(days=1)
        },
        {
            "name": "Client Meeting",
            "status": models.TaskStatus.ON_HOLD,
            "customer_name": "Acme Corp",
            "stakeholders": "John Doe",
            "useful_links": "https://zoom.us/j/123456",
            "comments": "Waiting for client availability.",
            "due_date": datetime.utcnow() - timedelta(hours=5)
        }
    ]

    for task_data in sample_tasks:
        db_task = models.Task(**task_data)
        db.add(db_task)
    
    db.commit()
    db.close()
    print("Sample data seeded successfully!")

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    seed_data()

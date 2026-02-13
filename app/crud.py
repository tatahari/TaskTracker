from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100, search: str = None, status: str = None):
    query = db.query(models.Task)
    if search:
        query = query.filter(
            or_(
                models.Task.name.ilike(f"%{search}%"),
                models.Task.customer_name.ilike(f"%{search}%"),
                models.Task.stakeholders.ilike(f"%{search}%")
            )
        )
    if status:
        query = query.filter(models.Task.status == status)
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    logger.info(f"CRUD delete_task called with task_id: {task_id}")
    db_task = get_task(db, task_id)
    logger.info(f"Task found: {db_task is not None}")
    if db_task:
        logger.info(f"Deleting task: {db_task.id} - {db_task.name}")
        db.delete(db_task)
        db.commit()
        logger.info(f"Task {task_id} successfully deleted")
        return True
    logger.warning(f"Task {task_id} not found for deletion")
    return False

def bulk_delete_tasks(db: Session, task_ids: List[int]):
    logger.info(f"CRUD bulk_delete_tasks called with task_ids: {task_ids}")
    try:
        count = db.query(models.Task).filter(models.Task.id.in_(task_ids)).delete(synchronize_session=False)
        db.commit()
        logger.info(f"Successfully deleted {count} tasks")
    except Exception as e:
        logger.error(f"Error in bulk_delete_tasks: {str(e)}", exc_info=True)
        raise

def bulk_update_status(db: Session, task_ids: List[int], status: models.TaskStatus):
    db.query(models.Task).filter(models.Task.id.in_(task_ids)).update({models.Task.status: status}, synchronize_session=False)
    db.commit()

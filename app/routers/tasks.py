from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List, Annotated
from ..database import get_db
from .. import crud, models, schemas
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["tasks"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks, "now": datetime.utcnow()})

@router.get("/tasks", response_class=HTMLResponse)
def list_tasks(request: Request, search: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, search=search, status=status)
    return templates.TemplateResponse("task_list_rows.html", {"request": request, "tasks": tasks, "now": datetime.utcnow()})

@router.get("/tasks/new", response_class=HTMLResponse)
def new_task_form(request: Request):
    return templates.TemplateResponse("task_form.html", {"request": request, "task": None})

@router.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
def edit_task_form(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    return templates.TemplateResponse("task_form.html", {"request": request, "task": task})

@router.post("/tasks/{task_id}/delete", response_class=HTMLResponse)
def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    logger.info(f"Delete request received for task_id: {task_id}")
    try:
        result = crud.delete_task(db, task_id)
        logger.info(f"Delete result for task {task_id}: {result}")
        tasks = crud.get_tasks(db)
        logger.info(f"Returning {len(tasks)} remaining tasks after delete")
        return templates.TemplateResponse("task_list_rows.html", {"request": request, "tasks": tasks, "now": datetime.utcnow()})
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}", exc_info=True)
        raise

@router.post("/tasks/bulk-delete", response_class=HTMLResponse)
def bulk_delete(request: Request, task_ids: Annotated[List[int], Form()], db: Session = Depends(get_db)):
    logger.info(f"Bulk delete request for task_ids: {task_ids}")
    try:
        crud.bulk_delete_tasks(db, task_ids)
        tasks = crud.get_tasks(db)
        logger.info(f"Bulk delete completed, {len(tasks)} tasks remaining")
        return templates.TemplateResponse("task_list_rows.html", {"request": request, "tasks": tasks, "now": datetime.utcnow()})
    except Exception as e:
        logger.error(f"Error in bulk delete: {str(e)}", exc_info=True)
        raise

@router.post("/tasks/bulk-status", response_class=HTMLResponse)
def bulk_status(request: Request, task_ids: Annotated[List[int], Form()], status: str = Form(...), db: Session = Depends(get_db)):
    if status:
        crud.bulk_update_status(db, task_ids, models.TaskStatus(status))
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("task_list_rows.html", {"request": request, "tasks": tasks, "now": datetime.utcnow()})

@router.post("/tasks", response_class=HTMLResponse)
def create_task(
    request: Request,
    name: str = Form(...),
    status: str = Form(...),
    priority: str = Form(...),
    customer_name: str = Form(None),
    stakeholders: str = Form(None),
    useful_links: str = Form(None),
    comments: str = Form(None),
    due_date: str = Form(None),
    db: Session = Depends(get_db)
):
    task_data = {
        "name": name,
        "status": status,
        "priority": priority,
        "customer_name": customer_name,
        "stakeholders": stakeholders,
        "useful_links": useful_links,
        "comments": comments,
        "due_date": datetime.fromisoformat(due_date) if due_date else None
    }
    crud.create_task(db, schemas.TaskCreate(**task_data))
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("task_list_rows.html", {"request": request, "tasks": tasks, "now": datetime.utcnow()})

@router.get("/tasks/{task_id}", response_class=HTMLResponse)
def task_detail(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("task_detail.html", {"request": request, "task": task, "now": datetime.utcnow()})

@router.post("/tasks/{task_id}", response_class=HTMLResponse)
def update_task(
    request: Request,
    task_id: int,
    name: str = Form(...),
    status: str = Form(...),
    priority: str = Form(...),
    customer_name: str = Form(None),
    stakeholders: str = Form(None),
    useful_links: str = Form(None),
    comments: str = Form(None),
    due_date: str = Form(None),
    db: Session = Depends(get_db)
):
    task_data = {
        "name": name,
        "status": status,
        "priority": priority,
        "customer_name": customer_name,
        "stakeholders": stakeholders,
        "useful_links": useful_links,
        "comments": comments,
        "due_date": datetime.fromisoformat(due_date) if due_date else None
    }
    crud.update_task(db, task_id, schemas.TaskUpdate(**task_data))
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("task_list_rows.html", {"request": request, "tasks": tasks, "now": datetime.utcnow()})

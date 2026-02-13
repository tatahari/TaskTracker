from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import pandas as pd
import io
from ..database import get_db
from .. import models

router = APIRouter(prefix="/exports", tags=["exports"])

@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    data = [
        {
            "ID": t.id,
            "Name": t.name,
            "Status": t.status.value,
            "Customer": t.customer_name,
            "Stakeholders": t.stakeholders,
            "Links": t.useful_links,
            "Comments": t.comments,
            "Due Date": t.due_date,
            "Created At": t.created_at
        } for t in tasks
    ]
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=tasks.csv"
    return response

@router.get("/excel")
def export_excel(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    data = [
        {
            "ID": t.id,
            "Name": t.name,
            "Status": t.status.value,
            "Customer": t.customer_name,
            "Stakeholders": t.stakeholders,
            "Links": t.useful_links,
            "Comments": t.comments,
            "Due Date": t.due_date,
            "Created At": t.created_at
        } for t in tasks
    ]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Tasks')
    
    output.seek(0)
    response = StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = "attachment; filename=tasks.xlsx"
    return response

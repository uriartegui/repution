from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.collector import collect_all, collect_for_company
from app.models.company import Company

router = APIRouter(prefix="/collect", tags=["collect"])


@router.post("/")
def trigger_collect_all(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Dispara coleta para todas as empresas em background."""
    background_tasks.add_task(collect_all, db)
    return {"message": "Coleta iniciada para todas as empresas"}


@router.post("/{company_id}")
def trigger_collect_company(
    company_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Dispara coleta para uma empresa específica."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        return {"error": "Empresa não encontrada"}
    background_tasks.add_task(collect_for_company, company, db)
    return {"message": f"Coleta iniciada para {company.name}"}

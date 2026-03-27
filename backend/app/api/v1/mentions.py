from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ai import classify_mention, generate_response
from app.models.mention import Mention
from app.schemas.mention import MentionCreate, MentionOut

router = APIRouter(prefix="/mentions", tags=["mentions"])


@router.post("/", response_model=MentionOut)
def create_mention(data: MentionCreate, db: Session = Depends(get_db)):
    mention = Mention(**data.model_dump())

    # Classifica com IA
    try:
        classification = classify_mention(data.content)
        mention.sentiment = classification.get("sentiment")
        mention.mention_type = classification.get("type")
        mention.reputation_score = classification.get("score")
        mention.ai_summary = classification.get("summary")
        mention.suggested_response = generate_response(data.content)
    except Exception as e:
        print(f"Erro na classificação IA: {e}")

    db.add(mention)
    db.commit()
    db.refresh(mention)
    return mention


@router.get("/", response_model=list[MentionOut])
def list_mentions(company_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Mention)
    if company_id:
        query = query.filter(Mention.company_id == company_id)
    return query.order_by(Mention.collected_at.desc()).all()


@router.get("/{mention_id}", response_model=MentionOut)
def get_mention(mention_id: int, db: Session = Depends(get_db)):
    mention = db.query(Mention).filter(Mention.id == mention_id).first()
    if not mention:
        raise HTTPException(status_code=404, detail="Menção não encontrada")
    return mention

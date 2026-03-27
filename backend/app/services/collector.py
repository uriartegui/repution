import time
import json
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.mention import Mention
from app.models.company import Company
from app.core.ai import classify_mention, generate_response
from app.services.scraper_reclame_aqui import fetch_reclame_aqui


def collect_for_company(company: Company, db: Session) -> int:
    keywords = []

    if company.keywords:
        try:
            keywords = json.loads(company.keywords)
        except Exception:
            keywords = [company.keywords]
    else:
        keywords = [company.name]

    is_first_collection = company.last_collected_at is None
    max_pages = 20 if is_first_collection else 3

    # Na primeira coleta passa vazio pra pegar tudo; depois passa os existentes pra parar cedo
    existing_urls = set()
    if not is_first_collection:
        existing_urls = set(
            r[0] for r in db.query(Mention.source_url)
            .filter(Mention.company_id == company.id, Mention.source_url != None)
            .all()
        )

    # URLs no banco pra deduplicar na inserção (sempre)
    all_existing_urls = set(
        r[0] for r in db.query(Mention.source_url)
        .filter(Mention.company_id == company.id, Mention.source_url != None)
        .all()
    )

    collected = 0

    for keyword in keywords:
        raw_mentions = fetch_reclame_aqui(keyword, existing_urls=existing_urls, max_pages=max_pages)

        for raw in raw_mentions:
            if raw.get("source_url") and raw["source_url"] in all_existing_urls:
                continue

            mention = Mention(
                company_id=company.id,
                source=raw["source"],
                source_url=raw.get("source_url"),
                author=raw.get("author"),
                content=raw["content"],
            )

            try:
                classification = classify_mention(raw["content"])
                mention.sentiment = classification.get("sentiment")
                mention.mention_type = classification.get("type")
                mention.reputation_score = classification.get("score")
                mention.ai_summary = classification.get("summary")
                mention.suggested_response = generate_response(raw["content"])
            except Exception as e:
                print(f"Erro na IA: {e}")

            time.sleep(2)
            db.add(mention)
            if raw.get("source_url"):
                all_existing_urls.add(raw["source_url"])
            collected += 1

    company.last_collected_at = datetime.now(timezone.utc)
    db.commit()
    return collected



def collect_all(db: Session) -> dict:
    companies = db.query(Company).all()
    results = {}
    for company in companies:
        count = collect_for_company(company, db)
        results[company.name] = count
    return results

from apscheduler.schedulers.background import BackgroundScheduler
from app.core.database import SessionLocal
from app.services.collector import collect_all

scheduler = BackgroundScheduler()


def run_collection():
    print("[Scheduler] Iniciando coleta automática...")
    db = SessionLocal()
    try:
        results = collect_all(db)
        print(f"[Scheduler] Coleta concluída: {results}")
    except Exception as e:
        print(f"[Scheduler] Erro na coleta: {e}")
    finally:
        db.close()


def start_scheduler(interval_hours: int = 1):
    scheduler.add_job(run_collection, "interval", hours=interval_hours, id="collect_all")
    scheduler.start()
    print(f"[Scheduler] Rodando a cada {interval_hours}h")


def stop_scheduler():
    scheduler.shutdown()

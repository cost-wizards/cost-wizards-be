from cost_wiz.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()

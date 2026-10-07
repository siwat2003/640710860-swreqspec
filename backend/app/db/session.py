# สร้าง engine และ session ของฐานข้อมูล (CON-TECH-01)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    """ส่ง session ให้ API แต่ละตัว แล้วปิดเมื่อจบ"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

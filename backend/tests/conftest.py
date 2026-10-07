# เตรียมฐานข้อมูล SQLite ในหน่วยความจำให้ทุก test (ไม่ต้องมี PostgreSQL จริง)
from datetime import date, time, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import Base, Slot
from app.db.session import get_db
from app.main import app

# ผู้รับบริการที่ยืนยันตัวตนแล้ว HN 0001234
AUTH = {"Authorization": "Bearer verified:0001234"}


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False)()
    yield session
    session.close()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def make_slot(db):
    """สร้างช่วงเวลา 1 ช่วง ค่าเริ่มต้นคือพรุ่งนี้ 09.00 น. แพ็กเกจ BASIC"""
    def _make(start="09:00", remaining=1, capacity=None, days_from_today=1, package_code="BASIC"):
        h, m = map(int, start.split(":"))
        slot = Slot(
            slot_date=date.today() + timedelta(days=days_from_today),
            start_time=time(h, m),
            package_code=package_code,
            capacity=capacity if capacity is not None else max(remaining, 1),
            remaining=remaining,
        )
        db.add(slot)
        db.commit()
        db.refresh(slot)
        return slot
    return _make

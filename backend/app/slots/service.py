# คำนวณช่วงเวลาที่ว่าง (T-02)
# รองรับ FR-BKG-01, FR-BKG-06
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Slot

DAYS_AHEAD = 14  # แสดงช่วงเวลาล่วงหน้า (FR-BKG-01)


def list_available_slots(db: Session, package_code: str, date_from: date | None = None) -> list[Slot]:
    """คืนช่วงเวลาที่ยังมีที่นั่ง ของแพ็กเกจที่เลือก (FR-BKG-01, FR-BKG-06)"""
    start = date_from or date.today()
    end = start + timedelta(days=DAYS_AHEAD)
    stmt = (
        select(Slot)
        .where(Slot.package_code == package_code)
        .where(Slot.slot_date >= start, Slot.slot_date <= end)
        .where(Slot.remaining > 0)
        .order_by(Slot.slot_date, Slot.start_time)
    )
    return list(db.scalars(stmt))

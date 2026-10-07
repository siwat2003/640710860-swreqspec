# API ค้นช่วงเวลาว่าง GET /slots (T-02)
# รองรับ FR-BKG-01, FR-BKG-06
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.slots import service

router = APIRouter()


@router.get("/slots")
def get_slots(package_code: str, date_from: date | None = None, db: Session = Depends(get_db)):
    """รายการช่วงเวลาว่าง พร้อมที่นั่งคงเหลือ (FR-BKG-01)
    เปลี่ยน package_code แล้วได้ช่วงเวลาของแพ็กเกจนั้น (FR-BKG-06)"""
    slots = service.list_available_slots(db, package_code, date_from)
    return [
        {
            "slot_id": s.id,
            "slot_date": s.slot_date.isoformat(),
            "start_time": s.start_time.strftime("%H:%M"),
            "remaining": s.remaining,
        }
        for s in slots
    ]

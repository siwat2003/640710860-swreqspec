# บันทึกการจองและตัดที่นั่ง (T-03)
# รองรับ FR-BKG-04
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Booking, Slot


class SlotFullError(Exception):
    """ช่วงเวลาที่เลือกไม่มีที่นั่งเหลือแล้ว"""


def next_queue_no(db: Session, slot_date) -> str:
    """ออกหมายเลขคิวรูปแบบ A001 เริ่มนับใหม่ทุกวัน (FR-BKG-04)"""
    count = db.scalar(
        select(func.count()).select_from(Booking).where(Booking.booking_date == slot_date)
    )
    return f"A{count + 1:03d}"


def create_booking(db: Session, hn: str, slot_id: int) -> Booking:
    """ยืนยันการจอง: ตรวจที่นั่ง ตัดที่นั่ง บันทึกการจอง ออกหมายเลขคิว (FR-BKG-04)"""
    slot = db.get(Slot, slot_id)
    if slot is None:
        raise ValueError("ไม่พบช่วงเวลา")
    if slot.remaining < 0:
        raise SlotFullError(slot_id)

    slot.remaining -= 1
    booking = Booking(
        hn=hn,
        slot_id=slot.id,
        booking_date=slot.slot_date,
        queue_no=next_queue_no(db, slot.slot_date),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(db: Session, booking_id: int, hn: str) -> None:
    """ยกเลิกการจอง และคืนที่นั่งให้ช่วงเวลานั้น (FR-BKG-04)"""
    booking = db.get(Booking, booking_id)
    if booking is None or booking.hn != hn:
        raise ValueError("ไม่พบการจอง")
    slot = db.get(Slot, booking.slot_id)
    slot.remaining += 1
    booking.status = "CANCELLED"
    db.commit()

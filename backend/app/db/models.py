# ตารางของฟีเจอร์จองคิวตรวจสุขภาพ (T-01)
# รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01
from datetime import date, datetime, time, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Slot(Base):
    """ช่วงเวลาตรวจ และที่นั่งคงเหลือ (FR-BKG-01, FR-BKG-06, ASM-01)"""
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_date: Mapped[date] = mapped_column(Date, index=True)
    start_time: Mapped[time] = mapped_column(Time)
    package_code: Mapped[str] = mapped_column(String(20), index=True)
    capacity: Mapped[int] = mapped_column(Integer)
    remaining: Mapped[int] = mapped_column(Integer)


class Booking(Base):
    """การจอง 1 รายการ เก็บเฉพาะ HN ไม่เก็บเลขบัตรประชาชน (FR-BKG-04, IF-HIS-01)"""
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hn: Mapped[str] = mapped_column(String(20), index=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"))
    booking_date: Mapped[date] = mapped_column(Date, index=True)
    queue_no: Mapped[str | None] = mapped_column(String(20), nullable=True)  # รอ Q-02
    status: Mapped[str] = mapped_column(String(20), default="BOOKED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class AuditLog(Base):
    """บันทึกการเข้าถึงข้อมูลสุขภาพ (DOM-PDPA-01)"""
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String(50))
    hn: Mapped[str] = mapped_column(String(20))
    accessed_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

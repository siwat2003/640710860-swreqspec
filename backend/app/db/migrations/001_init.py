# migration แรก: สร้างทุกตาราง (T-01)
# รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01
from app.db.models import Base


def upgrade(engine):
    """สร้างตาราง slots, bookings, audit_logs"""
    Base.metadata.create_all(engine)

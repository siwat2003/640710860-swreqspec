# อ่านค่าตั้งระบบจากตัวแปรสภาพแวดล้อม (CON-TECH-01)
import os

# ระบบจริงตั้ง DATABASE_URL เป็น PostgreSQL ตาม CON-TECH-01
# เช่น postgresql+psycopg://user:pass@db:5432/checkup
# ค่าเริ่มต้นเป็น SQLite ไว้ลองรันใน Codespace เท่านั้น
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

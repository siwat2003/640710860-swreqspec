# ตรวจผลยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการ (IF-IDP-01)
from fastapi import Header, HTTPException

PREFIX = "Bearer verified:"


def get_verified_hn(authorization: str | None = Header(default=None)) -> str:
    """คืน HN ของผู้ที่ยืนยันตัวตนแล้ว ถ้ายังไม่ยืนยัน ตอบ 401 (IF-IDP-01)

    ตอนนี้จำลองระบบยืนยันตัวตน: token รูปแบบ "Bearer verified:<HN>"
    ระบบจริงต้องส่ง token ไปตรวจกับระบบยืนยันตัวตนของโรงพยาบาล
    """
    if not authorization or not authorization.startswith(PREFIX):
        raise HTTPException(status_code=401, detail="ยังไม่ได้ยืนยันตัวตน")
    return authorization[len(PREFIX):]

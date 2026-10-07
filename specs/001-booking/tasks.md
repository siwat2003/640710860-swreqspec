# Tasks: จองคิวตรวจสุขภาพ (Booking)
Spec ID: SPEC-BKG-001 (Draft v2) | อ้างอิง: plan.md v1 | สร้างด้วย /tasks เมื่อ 2569-09-23 แก้รอบที่ 1 แล้ว

สรุป: ทั้งหมด 12 task (หลังบ้าน 9 หน้าจอ 3) เสร็จแล้ว 3 task (T-01 ถึง T-03)
รอ Open Question 1 task (T-06 รอ Q-02)

---

### T-01 สร้างตาราง slots, bookings, audit_logs
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ task อื่นทุกตัว
- ไฟล์ที่แตะ: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration รันผ่าน และตาราง bookings ไม่มีคอลัมน์เลขบัตรประชาชน (national_id)
- สถานะ: เสร็จ

### T-02 สร้าง API ค้นช่วงเวลาว่าง GET /slots
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: test_AC_BKG_05 ผ่านที่ 200 คำขอแบบย่อส่วน
- สถานะ: เสร็จ

### T-03 สร้าง API จองคิว POST /bookings
- รองรับ: FR-BKG-04, IF-IDP-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py, backend/app/main.py, backend/tests/test_AC_BKG_01.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: test_AC_BKG_01 ผ่าน
- สถานะ: เสร็จ

### T-04 กันจองซ้ำวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py, backend/tests/test_AC_BKG_02.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: test ของ AC-BKG-02 ทั้งหมดผ่าน (รวม test_TC_BKG_02_* ถ้ามี)
- สถานะ: พร้อมทำ

### T-05 เสนอช่วงเวลาใกล้เคียง 3 ตัวเลือกเมื่อเต็ม
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/booking/router.py, backend/tests/test_AC_BKG_03.py
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: test_AC_BKG_03 ผ่าน
- สถานะ: พร้อมทำ

### T-06 ออกหมายเลขคิวและแสดงบนหน้าจอ
- รองรับ: FR-BKG-04
- ตรวจด้วย: AC-BKG-01 (ส่วน "แสดงหมายเลขคิว")
- ไฟล์ที่แตะ: backend/app/booking/service.py, frontend/src/pages/BookingResult.jsx
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: หน้าจอแสดงเลขคิวตามรูปแบบที่กำหนดใน spec
- สถานะ: รอ Q-02

### T-07 คิวส่งข้อความ และส่งซ้ำสูงสุด 3 ครั้ง (ASM-03)
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py, backend/tests/test_AC_BKG_04.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: test_AC_BKG_04 ผ่าน
- สถานะ: พร้อมทำ

### T-08 audit log ทุกการเข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/main.py, backend/tests/test_AC_BKG_06.py
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: test_AC_BKG_06 ผ่าน
- สถานะ: พร้อมทำ

### T-09 ค้น HN จากระบบ HIS ก่อนจอง
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ ตรวจด้วย test_IF_HIS_01 (จำลอง HIS)
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/tests/test_IF_HIS_01.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: test_IF_HIS_01 ผ่าน และไม่มีเลขบัตรประชาชนถูกเก็บในฐานข้อมูล
- สถานะ: พร้อมทำ

### T-10 หน้าจอเลือกแพ็กเกจและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ (FR-BKG-06 ยังไม่มี AC)
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/App.jsx, frontend/src/__tests__/SlotPicker.test.jsx
- ต้องทำหลัง: ไม่มี (ใช้ API จำลอง)
- เสร็จเมื่อ: test หน้าจอ: เปลี่ยนแพ็กเกจแล้วรายการช่วงเวลาเปลี่ยนตาม
- สถานะ: พร้อมทำ

### T-11 หน้าจอยืนยัน และแจ้ง "ช่วงเวลาเต็ม" พร้อม 3 ตัวเลือก
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: AC-BKG-03.test.jsx ผ่าน
- สถานะ: พร้อมทำ

### T-12 ต่อหน้าจอกับ API จริง
- รองรับ: FR-BKG-01, FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/api/client.js, frontend/src/pages/SlotPicker.jsx, frontend/src/pages/ConfirmBooking.jsx
- ต้องทำหลัง: T-02, T-05, T-11
- เสร็จเมื่อ: หน้าจอเรียก API จริง และ test ทั้งหลังบ้านและหน้าจอของ AC-BKG-03 ผ่าน
- สถานะ: พร้อมทำ

---

## ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03, T-06 |
| AC-BKG-02 | T-04 |
| AC-BKG-03 | T-05, T-11, T-12 |
| AC-BKG-04 | T-07 |
| AC-BKG-05 | T-02 |
| AC-BKG-06 | T-08 |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-01 (ตาราง audit_logs), T-08 |
| IF-IDP-01 | T-03 |
| IF-HIS-01 | T-01, T-09 |
| IF-NOT-01 | T-07 |

## สิ่งที่ยังไม่ทำ

- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001)? -> ถามเจ้าหน้าที่เวชระเบียน
  task ที่รอ: T-06

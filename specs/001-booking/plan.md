# Plan: จองคิวตรวจสุขภาพ (Booking)

> หมายเหตุ: Spec ปัจจุบัน Status: Draft v1 — ยังไม่ได้ผ่านขั้น Clarify (มี Open Questions). ควรยืนยันกับทีมก่อนดำเนินการต่อหรือให้ผมทำต่อแบบมีข้อสมมติหรือไม่

## 1. สรุปแนวทาง
- ฟีเจอร์ให้ผู้รับบริการที่ยืนยันตัวตนแล้ว เลือกแพ็กเกจ วัน และช่วงเวลาเพื่อจองคิวตรวจสุขภาพ และรับหมายเลขคิว
- ผู้ใช้หลัก: ผู้รับบริการ (client web/mobile) และเจ้าหน้าที่นัดหมาย/เวชระเบียน
- แนวทาง: บริการ backend ให้ API สำหรับค้น availability, สร้างการจอง, เก็บคิวส่งข้อความแบบ asynchronous และบันทึก audit log
- ความสำคัญ: ไม่เก็บเลขบัตรประชาชนในตารางการจอง (ตาม IF-HIS-01) และต้องรองรับ retry ของการส่งข้อความ (NFR-REL-02)
- ก่อนสร้าง ให้ทีมตอบ Open Questions (Q-01, Q-02) เพื่อหลีกเลี่ยงการเดาที่มีผลต่อโครงสร้างข้อมูลและพฤติกรรม

## 2. เทคโนโลยีที่ใช้

สิ่งที่เลือก | มาจาก | หมายเหตุ
---|---|---
Frontend: React (Vite) | ทีมเลือกเอง ไม่ได้มาจาก spec | Default ของรายวิชา
Backend: Python + FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | Default ของรายวิชา
Database: MySQL | CON-TECH-01 | ตาม constraint ฝ่าย IT
Auth: IDP integration (OIDC) | IF-IDP-01 | รับผลยืนยันตัวตนจากระบบยืนยันตัวตน
HIS lookup (read-only) | IF-HIS-01 | ค้นด้วยเลขบัตรประชาชน แต่เก็บในระบบด้วย HN เท่านั้น
Notification: Async queue (worker) -> SMS/LINE | IF-NOT-01, NFR-REL-02 | ไม่รอผลการส่ง, มี retry policy
Audit log store | DOM-PDPA-01 | เก็บอย่างน้อย 1 ปี

## 3. โมเดลข้อมูล (Entities & ฟิลด์หลัก)

- `TimeSlot` (รองรับ FR-BKG-01, FR-BKG-03, FR-BKG-06)
  - id (PK)
  - date (YYYY-MM-DD)
  - start_time, end_time
  - capacity (int) — จำนวนที่นั่งโควตาต่อช่วง
  - remaining (int) — อัพเดตเมื่อจอง/ยกเลิก
  - compatible_packages (list/ref) — ถ้าจำเป็นสำหรับ FR-BKG-06

- `Package` (รองรับ FR-BKG-06)
  - id, name, duration_minutes, slot_units (ถ้าแพ็กเกจยืด/สั้นลง)

- `Booking` (รองรับ FR-BKG-02, FR-BKG-04, FR-BKG-05)
  - id (PK)
  - hn (ref to HIS HN)  -- ไม่เก็บเลขบัตรประชาชน (IF-HIS-01)
  - package_id, timeslot_id
  - status (enum: booked, checked_in, completed, cancelled, no_show)
  - queue_number (string/int)
  - created_at, confirmed_at

- `User` / `PatientRef` (รองรับ IF-HIS-01)
  - hn (PK), display_name, contact_methods (phone, line_id)
  - note: source of truth = HIS; พื้นที่จัดเก็บในระบบเก็บ HN ไม่เก็บเลขบัตรประชาชน

- `NotificationQueue` (รองรับ FR-BKG-05, NFR-REL-02, IF-NOT-01)
  - id, booking_id, payload, attempts, next_attempt_at, status

- `AuditLog` (รองรับ DOM-PDPA-01, AC-BKG-06)
  - id, actor_id, action, target_booking_id, timestamp, details

## 4. API / หน้าจอ (หลัก)

- GET /api/availability?start_date=YYYY-MM-DD&days=30&package_id=...  -> list of `TimeSlot` with remaining (FR-BKG-01)
- POST /api/bookings  { hn, package_id, timeslot_id } -> 201 { booking_id, queue_number } (FR-BKG-04, FR-BKG-02)
- GET /api/bookings/{booking_id} -> booking detail (show queue number) (FR-BKG-04, AC-BKG-01)
- GET /api/users/{hn}/bookings?date=YYYY-MM-DD -> list current day bookings (FR-BKG-02)
- POST /api/notifications/retry (worker endpoint) -> process NotificationQueue (FR-BKG-05, NFR-REL-02)

หน้าจอ (UI)
- หน้าเลือกแพ็กเกจและวันที่/ช่วงเวลา (map to GET availability) — รองรับ FR-BKG-01, FR-BKG-06
- หน้ายืนยันการจอง (POST /api/bookings) — แสดง queue number เมื่อสำเร็จ (FR-BKG-04)
- หน้าผล (confirmation) — แสดงหมายเลขคิวและข้อความยืนยัน (FR-BKG-05)

## 5. ตารางตรวจ Constraints

Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ
---|---|---
CON-TECH-01 | Database: MySQL (DB schema, migrations) | ใช้แล้ว
DOM-PDPA-01 | `AuditLog` เก็บการเข้าถึงการจองอย่างน้อย 1 ปี | ใช้แล้ว
IF-IDP-01 | Auth flow ต้องตรวจผลจาก IDP ก่อนเข้าถึง API | ใช้แล้ว
IF-HIS-01 | Lookup ผู้รับบริการจาก HIS โดยเลขบัตรประชาชน; เก็บ HN เป็น reference; ห้ามเก็บเลขบัตรประชาชนใน Booking | ใช้แล้ว
IF-NOT-01 | NotificationQueue + worker ส่งข้อความผ่าน SMS/LINE แบบ async | ใช้แล้ว

## 6. แผนทดสอบจาก Acceptance Criteria

AC ID | ชื่อ test | ทดสอบอย่างไร
---|---|---
AC-BKG-01 | test_AC_BKG_01_booking_persist_and_queue_number | เตรียม timeslot ที่มี remaining=1, POST /api/bookings แล้วตรวจ DB ว่าบันทึก, queue_number ถูกสร้าง, remaining ลดเหลือ 0
AC-BKG-02 | test_AC_BKG_02_prevent_duplicate_same_day | สร้าง booking สำหรับ hn ในวันเดียวกันแล้วเรียก POST อีกครั้ง คาดว่า API ปฏิเสธและคืนหมายเลขคิวเดิม
AC-BKG-03 | test_AC_BKG_03_offer_alternatives_when_full | กรณี concurrent เงื่อนไข slots เหลือ 1 และมีคนยืนยันก่อน ให้ผู้กดยืนยันเห็นข้อความ "ช่วงเวลาเต็ม" และรายการตัวเลือก 3 ช่วงเวลา (no booking created)
AC-BKG-04 | test_AC_BKG_04_record_when_notification_fails | จำลองระบบ notification ไม่ตอบสนอง; ยืนยันแล้วต้องบันทึก booking แสดง queue_number และมีรายการใน NotificationQueue ที่กำหนดส่งภายใน 5 นาที
AC-BKG-05 | test_AC_BKG_05_availability_p95 | รัน load test ของ endpoint availability ภายใต้ 200 concurrent users วัด p95 <= 2s (แนะนำ stub external calls เช่น HIS/NOTIF)
AC-BKG-06 | test_AC_BKG_06_audit_log_on_access | เปิดดูข้อมูลการจองแล้วตรวจ `AuditLog` มีรายการที่ระบุผู้เข้าถึง เวลา และ HN

## 7. ลำดับงาน (ข้อย่อย 7 ขั้น)

1. ออกแบบ DB schema: `TimeSlot`, `Package`, `Booking`, `UserRef`, `NotificationQueue`, `AuditLog` (FR-BKG-01, FR-BKG-04, DOM-PDPA-01)
2. พัฒนา API availability (GET /api/availability) และ unit tests (AC-BKG-05, FR-BKG-01)
3. พัฒนา API สร้าง booking และ logic ตรวจสอบ duplicate-per-day + queue generation (FR-BKG-02, FR-BKG-04, AC-BKG-01/02)
4. พัฒนาระบบ NotificationQueue + worker และ retry policy (FR-BKG-05, NFR-REL-02)
5. เพิ่ม audit logging ใน endpoints ที่เกี่ยวข้อง (DOM-PDPA-01, AC-BKG-06)
6. ทำ integration กับ HIS lookup (read-only) และ IDP auth (IF-HIS-01, IF-IDP-01)
7. ทดสอบ performance และปรับ tuning (AC-BKG-05, NFR-PERF-01)

## 8. สิ่งที่ยังไม่ทำ (Open Questions)

- Q-01: "ช่วงเวลาใกล้เคียง" นับเฉพาะวันเดียวกัน หรือรวมวันถัดไปด้วย? — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ
- Q-02: หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง? — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ

---

ไฟล์นี้สร้างจาก `specs/001-booking/spec.md` (Draft v1). รอคำตอบ Open Questions ก่อนปรับรายละเอียดโครงสร้างที่ขึ้นกับคำตอบเหล่านั้น

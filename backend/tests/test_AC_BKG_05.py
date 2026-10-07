# test ของ T-02: ความเร็วการค้นหาช่วงเวลาว่าง แบบย่อส่วน
# AC-BKG-05 (NFR-PERF-01): p95 ไม่เกิน 2 วินาที
import time


def test_AC_BKG_05(client, make_slot):
    for i in range(10):
        make_slot(start=f"{8 + i:02d}:00", remaining=5)

    durations = []
    for _ in range(200):  # ย่อส่วน: เรียก 200 ครั้ง แทนผู้ใช้ 200 คน
        t0 = time.perf_counter()
        res = client.get("/slots", params={"package_code": "BASIC"})
        durations.append(time.perf_counter() - t0)
        assert res.status_code == 200

    durations.sort()
    p95 = durations[int(len(durations) * 0.95) - 1]
    assert p95 <= 2.0

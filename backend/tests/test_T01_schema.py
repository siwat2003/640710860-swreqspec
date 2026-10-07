# test ของ T-01: migration รันผ่าน และไม่มีคอลัมน์เลขบัตรประชาชน
# รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01
import importlib

from sqlalchemy import create_engine, inspect


def _upgrade_fresh_db():
    engine = create_engine("sqlite://")
    migration = importlib.import_module("app.db.migrations.001_init")
    migration.upgrade(engine)
    return inspect(engine)


def test_T01_tables_created():
    insp = _upgrade_fresh_db()
    assert set(insp.get_table_names()) >= {"slots", "bookings", "audit_logs"}


def test_T01_no_national_id():
    insp = _upgrade_fresh_db()
    columns = [c["name"] for c in insp.get_columns("bookings")]
    assert "national_id" not in columns
    assert "hn" in columns

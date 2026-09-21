import re
import operations  # pyright: ignore[reportMissingImports]
import pytest



def test_generate_new_id_admin_format():
    new_id = operations.generate_new_id_admin()
    assert re.fullmatch(r"A-\d{1,8}", new_id)


def test_generate_new_id_patient_format():
    new_id = operations.generate_new_id_patient()
    assert re.fullmatch(r"P-\d{1,8}", new_id)


def test_generate_new_id_doctor_format():
    new_id = operations.generate_new_id_doctor()
    assert re.fullmatch(r"DR-\d{1,8}", new_id)


@pytest.mark.xfail(reason="generate_new_id_* use random numbers with no "
                           "uniqueness check", strict=False)
def test_generate_new_id_patient_is_unique_across_many_calls():
    ids = [operations.generate_new_id_patient() for _ in range(500)]
    assert len(ids) == len(set(ids)), (
        "Two calls produced the same ID - random.randrange has no "
        "collision check against already-issued IDs."
    )


def test_generate_new_id_patient_retries_on_collision(monkeypatch):
    # P1-13/P1-15 fix: generate_new_id_patient(existing_ids=...) should keep
    # drawing a new number until it finds one that isn't already taken.
    calls = iter([1, 1, 2])  # first two draws collide with "P-1", third is free
    monkeypatch.setattr(operations.random, "randrange", lambda a, b: next(calls))
    new_id = operations.generate_new_id_patient(existing_ids=["P-1"])
    assert new_id == "P-2"


def test_generate_new_id_sequential_picks_highest_plus_one():
    # The spec'd generate_new_id(role, existing_users) - sequential,
    # zero-padded, based on the highest existing number for that role.
    existing = [{"user_id": "P-00000003"}, {"user_id": "P-00000001"}]
    new_id = operations.generate_new_id("Patient", existing)
    assert new_id == "P-00000004"


def test_find_record_by_id_with_dicts():
    records = [{"user_id": "P-1"}, {"user_id": "P-2"}]
    found = operations.find_record_by_id(records, "P-2")
    assert found == {"user_id": "P-2"}


def test_find_record_by_id_with_appointment_dicts():
    records = [{"appointment_id": "APT-1"}, {"appointment_id": "APT-2"}]
    found = operations.find_record_by_id(records, "APT-2")
    assert found == {"appointment_id": "APT-2"}


def test_find_record_by_id_returns_none_when_missing():
    records = [{"user_id": "P-1"}]
    assert operations.find_record_by_id(records, "P-999") is None


def test_find_record_by_id_with_objects():
    from models import Patient
    p = Patient("P-1", "Test", "1234", "555", "M", "1990-01-01", "t@gmail.com", "addr")
    found = operations.find_record_by_id([p], "P-1")
    assert found is p


def test_get_available_time_slots_returns_free_slots_only():
    # P1-14 fix: this used to never return anything at all, and never
    # checked existing appointments for a clash.
    doctor = {"user_id": "DR-1", "shift_start_time": "09:00", "shift_end_time": "12:00"}
    appointments = [
        {"doctor_id": "DR-1", "date": "2026-09-20", "start_time": "10:00", "status": "Scheduled"},
    ]
    slots = operations.get_available_time_slots(doctor, "2026-09-20", appointments)
    assert slots == ["09:00", "11:00"]


def test_get_available_time_slots_ignores_cancelled_appointments():
    doctor = {"user_id": "DR-1", "shift_start_time": "09:00", "shift_end_time": "11:00"}
    appointments = [
        {"doctor_id": "DR-1", "date": "2026-09-20", "start_time": "09:00", "status": "Cancelled"},
    ]
    slots = operations.get_available_time_slots(doctor, "2026-09-20", appointments)
    assert slots == ["09:00", "10:00"]


def test_get_available_time_slots_ignores_other_doctors_and_dates():
    doctor = {"user_id": "DR-1", "shift_start_time": "09:00", "shift_end_time": "11:00"}
    appointments = [
        {"doctor_id": "DR-2", "date": "2026-09-20", "start_time": "09:00", "status": "Scheduled"},
        {"doctor_id": "DR-1", "date": "2026-09-21", "start_time": "09:00", "status": "Scheduled"},
    ]
    slots = operations.get_available_time_slots(doctor, "2026-09-20", appointments)
    assert slots == ["09:00", "10:00"]


def test_is_duplicate_id_detects_existing_id():
    records = [{"user_id": "P-1"}, {"user_id": "P-2"}]
    assert operations.is_duplicate_id("P-1", records) is True
    assert operations.is_duplicate_id("P-999", records) is False


def test_is_valid_name_rejects_empty_or_blank():
    assert operations.is_valid_name("Jane") is True
    assert operations.is_valid_name("") is False
    assert operations.is_valid_name("   ") is False


def test_is_valid_duration_rejects_zero_and_negative():
    assert operations.is_valid_duration(30) is True
    assert operations.is_valid_duration(0) is False
    assert operations.is_valid_duration(-15) is False


def test_is_valid_price_rejects_negative():
    assert operations.is_valid_price(0) is True
    assert operations.is_valid_price(25.5) is True
    assert operations.is_valid_price(-1) is False
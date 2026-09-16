import re
import operations
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
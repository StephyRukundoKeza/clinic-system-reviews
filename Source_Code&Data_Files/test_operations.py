import operations


def test_generate_new_id_sequential_picks_highest_plus_one():
    existing = [{"user_id": "P-00000003"}, {"user_id": "P-00000001"}]
    new_id = operations.generate_new_id("Patient", existing)
    assert new_id == "P-00000004"


def test_generate_new_id_sequential_starts_at_one_when_empty():
    assert operations.generate_new_id("Doctor", []) == "DR-00000001"


def test_generate_new_id_sequential_two_calls_never_collide():
    # This is the actual bug the old random generators could hit: two new
    # records ending up with the same ID. The sequential generator can't,
    # because each new ID is derived from what's already in the list.
    patients = [{"user_id": "P-00000001"}]
    first_new_id = operations.generate_new_id("Patient", patients)
    patients.append({"user_id": first_new_id})
    second_new_id = operations.generate_new_id("Patient", patients)
    assert first_new_id != second_new_id


def test_generate_new_id_sequential_works_with_objects_not_just_dicts():
    from models import Doctor
    existing = [Doctor("DR-00000005", "Dr. Test", "1234", "55512345",
                        "Cardiology", "09:00", "17:00")]
    assert operations.generate_new_id("Doctor", existing) == "DR-00000006"


def test_generate_new_id_rejects_unknown_role():
    try:
        operations.generate_new_id("NotARole", [])
        assert False, "expected a ValueError for an unknown role"
    except ValueError:
        pass


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
    doctor = {"user_id": "DR-1", "shift_start_time": "09:00", "shift_end_time": "12:00"}
    appointments = [
        {"doctor_id": "DR-1", "date": "2026-09-20", "start_time": "10:00"},
    ]
    slots = operations.get_available_time_slots(doctor, "2026-09-20", appointments)
    assert "09:00 - 10:00" in slots
    assert "10:00 - 11:00" not in slots


def test_get_available_time_slots_ignores_other_doctors_and_dates():
    doctor = {"user_id": "DR-1", "shift_start_time": "09:00", "shift_end_time": "11:00"}
    appointments = [
        {"doctor_id": "DR-2", "date": "2026-09-20", "start_time": "09:00"},
        {"doctor_id": "DR-1", "date": "2026-09-21", "start_time": "09:00"},
    ]
    slots = operations.get_available_time_slots(doctor, "2026-09-20", appointments)
    assert slots == ["09:00 - 10:00", "10:00 - 11:00"]

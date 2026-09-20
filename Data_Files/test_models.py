import json
from models import User, Admin, Doctor, Patient, Appointment

def test_user_verify_pin():
    u = User("U-1", "Test User", "1234", "55512345")
    assert u.verify_pin("1234") is True
    assert u.verify_pin("0000") is False

def test_user_login():
    u = User("U-1", "Test User", "1234", "55512345")
    assert u.login("1234") is True
    assert u.login("0000") is False


def test_admin_to_dict_is_json_serializable():
    a = Admin("A-00000001", "Admin Person", "1111", "55512345")
    data = a.to_dict()
    assert data["role"] == "Admin"
    json.dumps(data)

def test_doctor_to_dict_and_update_shifts():
    d = Doctor("DR-00000001", "Dr. Test", "2222", "55512345",
               "Cardiology", "09:00", "17:00")
    data = d.to_dict()
    assert data["role"] == "Doctor"
    assert data["shift_start_time"] == "09:00"
    assert data["shift_end_time"] == "17:00"
    json.dumps(data)

    d.update_shifts("10:00", "18:00")
    assert d.shift_start_time == "10:00"
    assert d.shift_end_time == "18:00"


def test_patient_to_dict_and_update_profile():
    p = Patient("P-00000001", "Pat Ient", "3333", "55512345",
                "Female", "1995-05-05", "pat@gmail.com", "123 Main St")
    data = p.to_dict()
    assert data["role"] == "Patient"
    json.dumps(data)

    p.update_profile(name="New Name")
    assert p.name == "New Name"
    assert p.address == "123 Main St"


def test_patient_notifications():
    p = Patient("P-00000002", "Notify Test", "4444", "55512345",
                "Male", "1990-01-01", "notify@gmail.com", "456 Elm St")
    assert p.notification is None

    p.add_notification("Your appointment is tomorrow")
    assert p.notification == ["Your appointment is tomorrow"]

    p.clear_notification()
    assert p.notification == []

def test_appointment_to_dict_and_reschedule():
    appt = Appointment("APT-000001", "P-00000001", "DR-00000001",
                        "2026-09-20", "10:00", duration_minutes=30)
    data = appt.to_dict()
    assert data["status"] == "Active"
    assert data["duration"] == 30
    json.dumps(data)

    appt.reschedule_appointment("2026-09-21", "11:00")
    assert appt.date == "2026-09-21"
    assert appt.start_time == "11:00"

    appt.update_status("Cancelled")
    assert appt.status == "Cancelled"
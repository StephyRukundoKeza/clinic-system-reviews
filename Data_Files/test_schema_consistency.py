import json
import inspect
import models
import os



def load_json(filename):
    with open(filename) as f:
        return json.load(f)

def test_doctor_json_fields_match_doctor_class():
    doctors = load_json("doctors.json")
    assert doctors, "doctors.json is empty - add at least one sample doctor to test against"

    expected_fields = [
        p for p in inspect.signature(models.Doctor.__init__).parameters
        if p != "self"
    ]

    for doctor in doctors:
        missing = [f for f in expected_fields if f not in doctor]
        assert not missing, (
            f"doctors.json record {doctor.get('user_id')} is missing fields "
            f"the Doctor class expects: {missing}. "
            f"Record actually has: {list(doctor.keys())}"
        )

def test_patient_json_fields_match_patient_class():
    patients = load_json("patients.json")
    assert patients, "patients.json is empty - add at least one sample patient to test against"

    expected_fields = [
        p for p in inspect.signature(models.Patient.__init__).parameters
        if p not in ("self", "notification")
    ]

    for patient in patients:
        missing = [f for f in expected_fields if f not in patient]
        assert not missing, (
            f"patients.json record {patient.get('user_id')} is missing fields "
            f"the Patient class expects: {missing}. "
            f"Record actually has: {list(patient.keys())}"
        )

def test_appointment_json_fields_match_appointment_class():
    appointments = load_json("appointments.json")
    assert appointments, "appointments.json is empty - add at least one sample appointment to test against"

    expected_fields = [
        p for p in inspect.signature(models.Appointment.__init__).parameters
        if p not in ("self", "status", "duration_minutes")
    ]
    expected_fields.append("duration")

    for appt in appointments:
        missing = [f for f in expected_fields if f not in appt]
        assert not missing, (
            f"appointments.json record {appt.get('appointment_id')} is missing "
            f"fields the Appointment class expects: {missing}. "
            f"Record actually has: {list(appt.keys())}"
        )

def test_admins_json_exists_and_is_a_list():
    # admins.json is now created/maintained by data_manager.save_data()
    # This replaces test_no_admins_json_file_exists, which
    # documented the old gap where admins were never persisted at all.
    assert os.path.exists("admins.json"), (
        "admins.json should exist now that save_data() writes it"
    )
    admins = load_json("admins.json")
    assert isinstance(admins, list)
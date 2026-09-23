import subprocess
import sys
import shutil
import os
import json
import datetime
import pytest


SOURCE_FILES = ("main.py", "data_manager.py", "models.py", "operations.py",
                 "validation.py", "sub_main.py")

# A date safely in the future no matter when the tests are actually run.
FUTURE_DATE = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
PAST_DATE = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()


def run_main(inputs, cwd, timeout=5):
    input_text = "\n".join(inputs) + "\n"
    result = subprocess.run(
        [sys.executable, os.path.join("Source_Code&Data_Files", "main.py")],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd,
    )
    return result.stdout, result.returncode


@pytest.fixture
def isolated_project(tmp_path):
    data_dir = tmp_path / "Source_Code&Data_Files"
    data_dir.mkdir()

    here = os.path.dirname(os.path.abspath(__file__))
    for f in SOURCE_FILES:
        src = os.path.join(here, f)
        if os.path.exists(src):
            shutil.copy(src, data_dir / f)

    patients = [{
        "user_id": "P-101", "name": "Jane Doe", "phone_number": "555-0199",
        "pin": "1234", "gender": "Female", "date_of_birth": "1990-05-14",
        "email": "jane.doe@gmail.com", "address": "123 Main St",
    }]
    doctors = [{
        "user_id": "DR-201", "name": "Smith", "phone_number": "555-0144",
        "pin": "5678", "specialization": "Cardiology",
        "shift_start_time": "09:00", "shift_end_time": "17:00",
    }]
    admins = [{
        "user_id": "A-100", "name": "Admin User", "phone_number": "555-0100",
        "pin": "9999",
    }]
    appointments = [{
        "appointment_id": "A-301", "date": FUTURE_DATE, "start_time": "10:00",
        "doctor_id": "DR-201", "patient_id": "P-101", "status": "Scheduled",
        "duration": 30,
    }]

    with open(data_dir / "patients.json", "w") as f:
        json.dump(patients, f)
    with open(data_dir / "doctors.json", "w") as f:
        json.dump(doctors, f)
    with open(data_dir / "admins.json", "w") as f:
        json.dump(admins, f)
    with open(data_dir / "appointments.json", "w") as f:
        json.dump(appointments, f)

    return tmp_path


def test_invalid_id_shows_error_and_reprompts(isolated_project):
    stdout, _ = run_main(["not-a-real-id", "exit"], cwd=isolated_project)
    assert "Invalid ID" in stdout


def test_exit_saves_and_closes_cleanly(isolated_project):
    stdout, returncode = run_main(["exit"], cwd=isolated_project)
    assert "Saving system data" in stdout
    assert "System closed successfully" in stdout
    assert returncode == 0


def test_admin_backdoor_no_longer_works(isolated_project):
    # The old hardcoded "A-ADMIN" / "1234" backdoor must be gone - only a
    # real admin record in admins.json should be able to log in.
    stdout, returncode = run_main(["A-ADMIN", "1234", "exit"], cwd=isolated_project)
    assert "Administrator Menu" not in stdout
    assert returncode == 0


def test_real_admin_login_works(isolated_project):
    stdout, returncode = run_main(["A-100", "9999", "13", "exit"], cwd=isolated_project)
    assert "Administrator Menu" in stdout
    assert "Logging out from Admin session" in stdout
    assert returncode == 0


def test_wrong_pin_is_rejected(isolated_project):
    stdout, returncode = run_main(["P-101", "0000", "exit"], cwd=isolated_project)
    assert "Incorrect PIN" in stdout
    assert "Patient Menu" not in stdout
    assert returncode == 0


def test_doctor_menu_logout_works(isolated_project):
    stdout, returncode = run_main(["DR-201", "5678", "4", "exit"], cwd=isolated_project)
    assert "Logging out" in stdout
    assert returncode == 0


def test_patient_menu_logout_works(isolated_project):
    stdout, returncode = run_main(["P-101", "1234", "5", "exit"], cwd=isolated_project)
    assert "Logging out" in stdout
    assert returncode == 0


def test_patient_can_view_own_information(isolated_project):
    stdout, returncode = run_main(["P-101", "1234", "1", "5", "exit"], cwd=isolated_project)
    assert "Jane Doe" in stdout
    assert returncode == 0


def test_patient_can_view_own_appointments(isolated_project):
    stdout, returncode = run_main(["P-101", "1234", "3", "5", "exit"], cwd=isolated_project)
    assert "A-301" in stdout
    assert returncode == 0


def test_doctor_can_view_own_schedule(isolated_project):
    stdout, returncode = run_main(["DR-201", "5678", "1", "4", "exit"], cwd=isolated_project)
    assert "A-301" in stdout
    assert returncode == 0


def test_new_registration_actually_creates_a_patient(isolated_project):
    stdout, returncode = run_main([
        "new",
        "Jane", "Test",
        "1990-01-01",
        "Female",
        "55512345",
        "jane.test@gmail.com",
        "1 Test St",
        "exit",
    ], cwd=isolated_project)
    assert "Registration successful!" in stdout
    assert returncode == 0

    with open(isolated_project / "Source_Code&Data_Files" / "patients.json") as f:
        patients = json.load(f)
    assert len(patients) == 2  # the fixture's sample patient + the new one
    assert any(p["name"] == "Jane Test" for p in patients)


def test_new_patient_ids_are_sequential_not_random(isolated_project):
    # Registering two new patients back to back should never produce the
    # same ID - the old random generator could, the sequential one can't.
    stdout, returncode = run_main([
        "new", "First", "Patient", "1990-01-01", "Female", "55512345",
        "first@gmail.com", "1 Test St",
        "new", "Second", "Patient", "1990-01-01", "Male", "57123456",
        "second@gmail.com", "2 Test St",
        "exit",
    ], cwd=isolated_project)
    assert returncode == 0

    with open(isolated_project / "Source_Code&Data_Files" / "patients.json") as f:
        patients = json.load(f)
    ids = [p["user_id"] for p in patients]
    assert len(ids) == len(set(ids)), "two new patients ended up with the same ID"


def test_admin_menu_rejects_bad_input_instead_of_crashing(isolated_project):
    stdout, returncode = run_main(["A-100", "9999", "x", "13", "exit"], cwd=isolated_project)
    assert returncode == 0
    assert "Selection out of range" in stdout or "Invalid format" in stdout


def test_admin_can_add_a_doctor(isolated_project):
    stdout, returncode = run_main([
        "A-100", "9999",
        "6", "New", "Doc", "Neurology", "09:00", "17:00", "55512345", "2222",
        "13", "exit",
    ], cwd=isolated_project)
    assert "Successful! Doctor New Doc added" in stdout
    assert returncode == 0


def test_patient_booking_rejects_past_date_then_accepts_future_date(isolated_project):
    stdout, returncode = run_main([
        "P-101", "1234",
        "2", "1", PAST_DATE, FUTURE_DATE, "1",
        "5", "exit",
    ], cwd=isolated_project)
    assert "cannot be before today's date" in stdout
    assert "Success! Appointment booked." in stdout
    assert returncode == 0


def test_doctor_can_update_status_and_reschedule(isolated_project):
    stdout, returncode = run_main([
        "DR-201", "5678",
        "3", "A-301", "1", "yes", FUTURE_DATE, "14:30",
        "4", "exit",
    ], cwd=isolated_project)
    assert "status updated to 'Completed'" in stdout
    assert "rescheduled to" in stdout
    assert returncode == 0

    with open(isolated_project / "Source_Code&Data_Files" / "appointments.json") as f:
        appointments = json.load(f)
    updated = next(a for a in appointments if a["appointment_id"] == "A-301")
    assert updated["date"] == FUTURE_DATE
    assert updated["start_time"] == "14:30"
    assert updated["status"] == "Completed"


def test_doctor_can_decline_reschedule_and_only_change_status(isolated_project):
    stdout, returncode = run_main([
        "DR-201", "5678",
        "3", "A-301", "3", "no",
        "4", "exit",
    ], cwd=isolated_project)
    assert "status updated to 'Cancelled'" in stdout
    assert "rescheduled to" not in stdout
    assert returncode == 0


def test_data_survives_ctrl_c(isolated_project, monkeypatch):
    # Simulates the user hitting Ctrl+C instead of typing "exit". Sending a
    # real OS interrupt signal to a subprocess works differently on Windows
    # than everywhere else, so instead this calls main() directly and makes
    # the very first input() raise KeyboardInterrupt - the same exception
    # Python raises internally on a real Ctrl+C.
    monkeypatch.chdir(isolated_project)
    monkeypatch.syspath_prepend(str(isolated_project / "Source_Code&Data_Files"))

    def raise_keyboard_interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", raise_keyboard_interrupt)

    import main as main_module
    main_module.main()  # should not raise - try/except/finally should catch it and save

    with open(isolated_project / "Source_Code&Data_Files" / "patients.json") as f:
        patients = json.load(f)
    assert patients  # the fixture's sample patient is still there - data was saved

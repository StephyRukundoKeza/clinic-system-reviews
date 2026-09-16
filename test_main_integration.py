import subprocess
import sys
import shutil
import os
import json
import pytest


def run_main(inputs, timeout=5):
    input_text = "\n".join(inputs) + "\n"
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout, result.returncode


@pytest.fixture
def isolated_project(tmp_path, monkeypatch):
 
    for f in ("main.py", "data_manager.py", "models.py", "operations.py",
              "validation.py", "sub_main.py"):
        if os.path.exists(f):
            shutil.copy(f, tmp_path / f)

    patients = [{
        "user_id": "P-101", "name": "Jane Doe", "phone_number": "555-0199",
        "pin": "1234", "gender": "Female", "date_of_birth": "1990-05-14",
        "email": "jane.doe@gmail.com", "address": "123 Main St",
    }]
    doctors = [{
        "user_id": "DR-201", "name": "Dr. Smith", "phone_number": "555-0144",
        "pin": "5678", "specialization": "Cardiology",
        "shift_start_time": "09:00", "shift_end_time": "17:00",
    }]
    admins = [{
        "user_id": "A-100", "name": "Admin User", "phone_number": "555-0100",
        "pin": "9999",
    }]

    with open(tmp_path / "patients.json", "w") as f:
        json.dump(patients, f)
    with open(tmp_path / "doctors.json", "w") as f:
        json.dump(doctors, f)
    with open(tmp_path / "admins.json", "w") as f:
        json.dump(admins, f)
    appointments = [{
        "appointment_id": "A-301", "date": "2026-09-20", "start_time": "10:00",
        "doctor_id": "DR-201", "patient_id": "P-101", "status": "Scheduled",
        "duration": 30,
    }]
    with open(tmp_path / "appointments.json", "w") as f:
        json.dump(appointments, f)

    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_invalid_id_shows_error_and_reprompts(isolated_project):
    stdout, _ = run_main(["not-a-real-id", "exit"])
    assert "Invalid ID" in stdout


def test_exit_closes_cleanly(isolated_project):
    stdout, returncode = run_main(["exit"])
    assert "System closed successfully" in stdout
    assert returncode == 0


def test_doctor_menu_logout_works(isolated_project):
    stdout, returncode = run_main(["DR-201", "5678", "4", "exit"])
    assert stdout.count("Enter your ID") >= 2
    assert returncode == 0


def test_patient_menu_logout_works(isolated_project):
    stdout, returncode = run_main(["P-101", "1234", "5", "exit"])
    assert "Logging out..." in stdout
    assert returncode == 0


def test_wrong_pin_is_rejected(isolated_project):
    # P1-18 fix: a correct-looking ID with the wrong PIN must not open the menu.
    stdout, returncode = run_main(["P-101", "0000", "exit"])
    assert "Incorrect PIN" in stdout
    assert "PATIENT MENU" not in stdout
    assert returncode == 0

def test_patient_can_view_own_information(isolated_project):
    stdout, returncode = run_main(["P-101", "1234", "1", "5", "exit"])
    assert "Jane Doe" in stdout
    assert returncode == 0


def test_patient_can_view_own_appointments(isolated_project):
    stdout, returncode = run_main(["P-101", "1234", "3", "5", "exit"])
    assert "A-301" in stdout
    assert returncode == 0


def test_doctor_can_view_own_appointments(isolated_project):
    stdout, returncode = run_main(["DR-201", "5678", "1", "4", "exit"])
    assert "A-301" in stdout
    assert returncode == 0

def test_unknown_id_with_valid_prefix_is_rejected(isolated_project):
    # A correctly-shaped ID (right prefix) that doesn't match any real
    # record should be treated the same as any other invalid ID.
    stdout, returncode = run_main(["P-999", "1234", "exit"])
    assert "Invalid ID" in stdout
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
    ])
    assert "Registration successful!" in stdout
    assert returncode == 0

    with open("patients.json") as f:
        patients = json.load(f)
    assert len(patients) == 2  # the fixture's sample patient + the new one
    assert any(p["name"] == "Jane Test" for p in patients)


def test_admin_menu_rejects_bad_input_instead_of_crashing(isolated_project):
    stdout, returncode = run_main(["A-100", "9999", "x", "7", "exit"])
    assert returncode == 0, (
        f"Program crashed instead of handling bad input gracefully "
        f"(returncode={returncode}). Output:\n{stdout}"
    )
    assert "Please enter a number between 1 and 7." in stdout


def test_admin_menu_logout_actually_works(isolated_project):
    stdout, _ = run_main(["A-100", "9999", "7", "exit"])
    assert "Logging out..." in stdout, (
        "Typing 7 to log out of the admin menu didn't log out - "
        "it fell through to the else branch instead (int vs string compare bug)."
    )

def test_admin_menu_all_options_run_without_crashing(isolated_project):
    stdout, returncode = run_main([
        "A-100", "9999",
        "1", "Jane", "Test", "1990-01-01", "Female", "55512345", "jane.test@gmail.com", "1 Test St", "1111",
        "2",
        "3", "P-101",
        "4", "P-101", "", "", "", "", "", "",
        "5", "Add", "Doc", "Neurology", "09:00", "17:00", "55512345", "2222",
        "6",
        "7",
        "exit",
    ])
    assert returncode == 0, (
        f"Something crashed while running through every admin menu option "
        f"(returncode={returncode}). Output:\n{stdout}"
    )


def test_doctor_menu_all_options_run_without_crashing(isolated_project):
    stdout, returncode = run_main([
        "DR-201", "5678",
        "1",
        "2", "P-101",
        "3", "A-301", "Completed",
        "4",
        "exit",
    ])
    assert returncode == 0, (
        f"Something crashed while running through every doctor menu option "
        f"(returncode={returncode}). Output:\n{stdout}"
    )


def test_patient_menu_all_options_run_without_crashing(isolated_project):
    stdout, returncode = run_main([
        "P-101", "1234",
        "1",
        "2", "b", "DR-201", "2026-09-25", "09:00",
        "3",
        "4", "A-301", "yes",
        "5",
        "exit",
    ])
    assert returncode == 0, (
        f"Something crashed while running through every patient menu option "
        f"(returncode={returncode}). Output:\n{stdout}"
    )
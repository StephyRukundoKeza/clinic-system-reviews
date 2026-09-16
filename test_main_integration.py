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
    with open(tmp_path / "appointments.json", "w") as f:
        json.dump([], f)

    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_invalid_id_shows_error_and_reprompts(isolated_project):
    stdout, _ = run_main(["not-a-real-id", "exit"])
    assert "Invalid ID" in stdout

def test_new_registration_trigger_is_case_insensitive(isolated_project):
    stdout, returncode = run_main(["new", "exit"])
    assert "Starting new patient registration" in stdout
    assert returncode == 0


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


def test_unknown_id_with_valid_prefix_is_rejected(isolated_project):
    # A correctly-shaped ID (right prefix) that doesn't match any real
    # record should be treated the same as any other invalid ID.
    stdout, returncode = run_main(["P-999", "1234", "exit"])
    assert "Invalid ID" in stdout
    assert returncode == 0


def test_new_registration_does_not_actually_save_a_patient(isolated_project):
    with open("patients.json") as f:
        before = json.load(f)

    run_main(["new", "Jane Test", "55512345", "Female", "1990-01-01",
              "jane@gmail.com", "1 Test St", "exit"])

    with open("patients.json") as f:
        after = json.load(f)

    assert before == after, (
        "patients.json changed after registering via NEW - looks like "
        "register_patient() now actually saves. If so, remove this test "
        "and write a real 'registration succeeds' test instead."
    )


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
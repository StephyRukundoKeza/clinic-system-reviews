import subprocess
import sys
import shutil
import os
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

def test_invalid_id_shows_error_and_reprompts():
    stdout, _ = run_main(["not-a-real-id", "exit"])
    assert "Invalid ID" in stdout


def test_exit_closes_cleanly():
    stdout, returncode = run_main(["exit"])
    assert "System closed successfully" in stdout
    assert returncode == 0

def test_doctor_menu_logout_works():
    stdout, returncode = run_main(["DR-11111111", "4", "exit"])
    assert stdout.count("Enter your ID:") >= 2
    assert returncode == 0


def test_patient_menu_logout_works():
    stdout, returncode = run_main(["P-11111111", "5", "exit"])
    assert "Logging out..." in stdout
    assert returncode == 0


def test_new_registration_does_not_actually_save_a_patient(tmp_path, monkeypatch):
    for f in ("main.py", "data_manager.py", "models.py", "operations.py",
              "validation.py", "sub_main.py", "patients.json", "doctors.json",
              "appointments.json"):
        if os.path.exists(f):
            shutil.copy(f, tmp_path / f)
    monkeypatch.chdir(tmp_path)

    with open("patients.json") as f:
        before = f.read()

    run_main(["new", "Jane Test", "55512345", "Female", "1990-01-01",
              "jane@gmail.com", "1 Test St", "exit"])

    with open("patients.json") as f:
        after = f.read()

    assert before == after, (
        "patients.json changed after registering via NEW - looks like "
        "register_patient() now actually saves. If so, remove this test "
        "and write a real 'registration succeeds' test instead."
    )

@pytest.mark.xfail(reason="admin_menu() crashes on non-numeric input - "
                           "no try/except around int(input())", strict=False)
def test_admin_menu_rejects_bad_input_instead_of_crashing():
    stdout, returncode = run_main(["A-11111111", "x", "exit"])
    assert returncode == 0, (
        f"Program crashed instead of handling bad input gracefully "
        f"(returncode={returncode}). Output:\n{stdout}"
    )
    assert "Invalid" in stdout or "valid number" in stdout.lower()


@pytest.mark.xfail(reason="admin_menu() compares an int choice against string "
                           "literals like \"7\", so logout never matches",
                    strict=False)
def test_admin_menu_logout_actually_works():
    stdout, _ = run_main(["A-11111111", "7", "exit"])
    assert "Logging out..." in stdout, (
        "Typing 7 to log out of the admin menu didn't log out - "
        "it fell through to the else branch instead (int vs string compare bug)."
    )
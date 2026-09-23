import json
import os
import pytest
import data_manager


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    # data_manager reads/writes under "Source_Code&Data_Files/", so the
    # cwd needs that folder to exist relative to it, same as the real repo.
    data_dir = tmp_path / "Source_Code&Data_Files"
    data_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_load_data_reads_existing_files(project_root):
    patients = [{"user_id": "P-00000001", "name": "Test Patient"}]
    doctors = [{"user_id": "DR-00000001", "name": "Test Doctor"}]
    appointments = [{"appointment_id": "APT-000001", "status": "Active"}]

    with open("Source_Code&Data_Files/patients.json", "w") as f:
        json.dump(patients, f)
    with open("Source_Code&Data_Files/doctors.json", "w") as f:
        json.dump(doctors, f)
    with open("Source_Code&Data_Files/appointments.json", "w") as f:
        json.dump(appointments, f)

    loaded_patients, loaded_doctors, loaded_appointments, loaded_admins = data_manager.load_data()
    assert loaded_patients == patients
    assert loaded_doctors == doctors
    assert loaded_appointments == appointments
    assert loaded_admins == []


def test_load_data_missing_files_returns_empty_lists(project_root):
    patients, doctors, appointments, admins = data_manager.load_data()
    assert patients == []
    assert doctors == []
    assert appointments == []
    assert admins == []


def test_save_data_round_trip(project_root):
    patients = [{"user_id": "P-00000001", "name": "Round Trip Patient"}]
    doctors = [{"user_id": "DR-00000001", "name": "Round Trip Doctor"}]
    appointments = [{"appointment_id": "APT-000001", "status": "Active"}]
    admins = [{"user_id": "A-00000001", "name": "Round Trip Admin"}]

    data_manager.save_data(patients, doctors, appointments, admins)

    assert os.path.exists("Source_Code&Data_Files/patients.json")
    assert os.path.exists("Source_Code&Data_Files/doctors.json")
    assert os.path.exists("Source_Code&Data_Files/appointments.json")
    assert os.path.exists("Source_Code&Data_Files/admins.json")

    loaded_patients, loaded_doctors, loaded_appointments, loaded_admins = data_manager.load_data()
    assert loaded_patients == patients
    assert loaded_doctors == doctors
    assert loaded_appointments == appointments
    assert loaded_admins == admins


def test_save_data_overwrites_previous_contents(project_root):
    data_manager.save_data([{"user_id": "P-1"}], [], [], [])
    data_manager.save_data([{"user_id": "P-2"}], [], [], [])

    patients, _, _, _ = data_manager.load_data()
    assert patients == [{"user_id": "P-2"}]


def test_save_data_serializes_model_objects(project_root):
    # save_data can be handed real Patient/Doctor/Admin/Appointment objects
    # (not just dicts) straight after they're created during a session.
    import models

    patient = models.Patient("P-1", "Obj Patient", "1234", "55512345",
                              "Female", "1990-01-01", "obj@gmail.com", "1 Obj St")
    data_manager.save_data([patient], [], [], [])

    with open("Source_Code&Data_Files/patients.json") as f:
        saved = json.load(f)
    assert saved[0]["user_id"] == "P-1"
    assert saved[0]["name"] == "Obj Patient"

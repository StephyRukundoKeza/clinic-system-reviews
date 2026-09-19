import json
import pytest
import data_manager
import os


@pytest.fixture
def temp_project_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    yield tmp_path

def test_load_data_reads_existing_files(temp_project_dir):
    patients = [{"user_id": "P-00000001", "name": "Test Patient"}]
    doctors = [{"user_id": "DR-00000001", "name": "Test Doctor"}]
    appointments = [{"appointment_id": "APT-000001", "status": "Active"}]

    with open("patients.json", "w") as f:
        json.dump(patients, f)
    with open("doctors.json", "w") as f:
        json.dump(doctors, f)
    with open("appointments.json", "w") as f:
        json.dump(appointments, f)

    loaded_patients, loaded_doctors, loaded_appointments, loaded_admins = data_manager.load_data()
    assert loaded_patients == patients
    assert loaded_doctors == doctors
    assert loaded_appointments == appointments
    assert loaded_admins == []

def test_load_data_missing_files_returns_empty_lists(temp_project_dir):
    patients, doctors, appointments,admins = data_manager.load_data()

    assert patients == []
    assert doctors == []
    assert appointments == []
    assert admins == []


def test_save_data_round_trip(temp_project_dir):
    patients = [{"user_id": "P-00000001", "name": "Round Trip Patient"}]
    doctors = [{"user_id": "DR-00000001", "name": "Round Trip Doctor"}]
    appointments = [{"appointment_id": "APT-000001", "status": "Active"}]
    admins = [{"user_id": "A-00000001", "name": "Round Trip Admin"}]

    data_manager.save_data(patients, doctors, appointments, admins)

    assert os.path.exists("patients.json")
    assert os.path.exists("doctors.json")
    assert os.path.exists("appointments.json")
    assert os.path.exists("admins.json")

    loaded_patients, loaded_doctors, loaded_appointments, loaded_admins = data_manager.load_data()
    assert loaded_patients == patients
    assert loaded_doctors == doctors
    assert loaded_appointments == appointments
    assert loaded_admins == admins

def test_save_data_overwrites_previous_contents(temp_project_dir):
    data_manager.save_data([{"user_id": "P-1"}], [], [], [])
    data_manager.save_data([{"user_id": "P-2"}], [], [], [])

    patients, _, _,_= data_manager.load_data()
    assert patients == [{"user_id": "P-2"}]


def test_save_data_persists_and_reloads_admins(temp_project_dir):
    admins = [{"user_id": "A-00000001", "name": "Test Admin"}]
    data_manager.save_data([], [], [], admins)

    _, _, _, loaded_admins = data_manager.load_data()
    assert loaded_admins == admins 
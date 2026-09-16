import json
import pytest
import data_manager
import os
import inspect


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

    loaded_patients, loaded_doctors, loaded_appointments = data_manager.load_data()

    assert loaded_patients == patients
    assert loaded_doctors == doctors
    assert loaded_appointments == appointments

def test_load_data_missing_files_returns_empty_lists(temp_project_dir):
    patients, doctors, appointments = data_manager.load_data()

    assert patients == []
    assert doctors == []
    assert appointments == []



def test_save_data_round_trip(temp_project_dir):
    patients = [{"user_id": "P-00000001", "name": "Round Trip Patient"}]
    doctors = [{"user_id": "DR-00000001", "name": "Round Trip Doctor"}]
    appointments = [{"appointment_id": "APT-000001", "status": "Active"}]

    data_manager.save_data(patients, doctors, appointments)

    assert os.path.exists("patients.json")
    assert os.path.exists("doctors.json")
    assert os.path.exists("appointments.json")

    loaded_patients, loaded_doctors, loaded_appointments = data_manager.load_data()
    assert loaded_patients == patients
    assert loaded_doctors == doctors
    assert loaded_appointments == appointments

def test_save_data_overwrites_previous_contents(temp_project_dir):
    data_manager.save_data([{"user_id": "P-1"}], [], [])
    data_manager.save_data([{"user_id": "P-2"}], [], [])

    patients, _, _ = data_manager.load_data()
    assert patients == [{"user_id": "P-2"}]


def test_save_data_has_no_admins_parameter():
    params = list(inspect.signature(data_manager.save_data).parameters)
    assert params == ["patients", "doctors", "appointments"], (
        "save_data()'s signature changed - if 'admins' was added, "
        "update this test to actually exercise admin persistence "
        "instead of just documenting the gap."
    )
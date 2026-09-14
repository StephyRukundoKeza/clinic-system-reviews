import json

def load_data():
    """
    Reads patients, doctors, and appointments from their respective JSON files.
    Returns empty lists if any file is missing to prevent application crashes.
    """
    # 1. Read patients.json
    try:
        with open('patients.json', 'r') as f:
            patients = json.load(f)
    except FileNotFoundError:
        patients = []

    # 2. Read doctors.json
    try:
        with open('doctors.json', 'r') as f:
            doctors = json.load(f)
    except FileNotFoundError:
        doctors = []

    # 3. Read appointments.json
    try:
        with open('appointments.json', 'r') as f:
            appointments = json.load(f)
    except FileNotFoundError:
        appointments = []

    return patients, doctors, appointments

def save_data(patients, doctors, appointments):
    """
    Writes patients, doctors, and appointments back to their respective JSON files.
    """
    # 1. Save patients.json
    with open('patients.json', 'w') as f:
        json.dump(patients, f, indent=4)

    # 2. Save doctors.json
    with open('doctors.json', 'w') as f:
        json.dump(doctors, f, indent=4)

    # 3. Save appointments.json
    with open('appointments.json', 'w') as f:
        json.dump(appointments, f, indent=4)
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


    # 4. Read admins.json
    try:
        with open('admins.json', 'r') as f:
            admins = json.load(f)
    except FileNotFoundError:
        admins = []

    return patients, doctors, appointments, admins

def _to_serializable(records):
    """
    A list saved during a session can contain a mix of plain dicts (loaded
    from JSON) and freshly-created model objects (Patient/Doctor/Admin/
    Appointment) - e.g. right after someone registers. json.dump() can't
    serialize those objects directly, so convert anything that has a
    to_dict() method before writing it out.
    """
    return [r.to_dict() if hasattr(r, "to_dict") else r for r in records]


def save_data(patients, doctors, appointments,admins):
    """
    Writes patients, doctors, and appointments back to their respective JSON files.
    """
    # 1. Save patients.json
    with open('patients.json', 'w') as f:
        json.dump(_to_serializable(patients), f, indent=4)

    # 2. Save doctors.json
    with open('doctors.json', 'w') as f:
        json.dump(_to_serializable(doctors), f, indent=4)

    # 3. Save appointments.json
    with open('appointments.json', 'w') as f:
        json.dump(_to_serializable(appointments), f, indent=4)

    # 4. Save admins.json
    with open('admins.json', 'w') as f:
        json.dump(_to_serializable(admins), f, indent=4)

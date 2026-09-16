print("Day one on clinic appointment system!")
import random

def is_duplicate_id(new_id, existing_records):
    """True if new_id already belongs to someone/something in existing_records."""
    for record in existing_records:
        record_id = record.get('user_id') if isinstance(record, dict) else getattr(record, 'user_id', None)
        if record_id == new_id:
            return True
    return False


def is_valid_name(name):
    """Business rule: a name can't be empty or just whitespace."""
    return isinstance(name, str) and name.strip() != ""


def is_valid_duration(duration_minutes):
    """Business rule: an appointment's duration must be a positive number of minutes."""
    return isinstance(duration_minutes, (int, float)) and duration_minutes > 0

def check_pin(record, input_pin):
    """True if input_pin matches this record's stored pin - record can be
    a dict (from JSON) or a User/Admin/Doctor/Patient object."""
    stored_pin = record.get('pin') if isinstance(record, dict) else getattr(record, 'pin', None)
    return stored_pin == input_pin


def is_valid_price(price):
    """Business rule: a price can't be negative. (No price field exists in the
    data model yet — this is ready for whenever one's added.)"""
    return isinstance(price, (int, float)) and price >= 0

def generate_new_id_admin(existing_ids=None):
    while True:
        id = random.randrange(00000000, 99999999)
        new_id = f"A-{id}"
        if not existing_ids or new_id not in existing_ids:
            print(f"Your admin id is {new_id}")
            return new_id

def generate_new_id_patient(existing_ids=None):
    # Generates a unique 8-digit ID for new patients (see note above).
    while True:
        id = random.randrange(00000000, 99999999)
        new_id = f"P-{id}"
        if not existing_ids or new_id not in existing_ids:
            print(f"Your patient id is {new_id}")
            return new_id

def generate_new_id_doctor(existing_ids=None):
    # Generates a unique 8-digit ID for new doctors (see note above).
    while True:
        id = random.randrange(00000000, 99999999)
        new_id = f"DR-{id}"
        if not existing_ids or new_id not in existing_ids:
            print(f"Your doctor id is {new_id}")
            return new_id

def generate_new_id(role, existing_users):
    """
    Generates the next sequential ID for a role: 'Patient' -> P-, 'Doctor' -> DR-, 'Admin' -> A-.
    Looks through existing_users (dicts or objects) for the highest number
    already used with that prefix, then returns highest + 1, zero-padded to 8 digits.
    """
    prefixes = {"Patient": "P-", "Doctor": "DR-", "Admin": "A-"}
    prefix = prefixes.get(role)
    if prefix is None:
        raise ValueError(f"Unknown role '{role}'. Expected one of: {list(prefixes.keys())}")

    highest_number = 0
    for user in existing_users:
        user_id = user.get('user_id') if isinstance(user, dict) else getattr(user, 'user_id', None)
        if user_id and user_id.startswith(prefix):
            number_part = user_id[len(prefix):]
            if number_part.isdigit():
                highest_number = max(highest_number, int(number_part))

    return f"{prefix}{highest_number + 1:08d}"

def find_record_by_id(record_list, search_id):
    for record in record_list:
# Check if the record is a dictionary (freshly loaded from JSON by Student 3)
        if isinstance(record, dict):
# We check 'user_id', but if it's an appointment, it falls back to checking 'appointment_id'
            record_id = record.get('user_id') or record.get('appointment_id')
            if record_id == search_id:
                return record
                
        # Check if the record is an Object (actively created during this session)
        else:
# Use getattr to safely check for the ID attribute without crashing
            record_id = getattr(record, 'user_id', None) or getattr(record, 'appointment_id', None)
            if record_id == search_id:
                return record
    
    # Return None if the loop finishes and no match was found
    return None

def generate_new_id_appointment():
# Generates a unique 6-digit ID for new appointments.
    id = random.randrange(100000, 999999)
    return f"APT-{id}"

from datetime import datetime, timedelta

def get_available_time_slots(doctor, target_date, appointment_list):
# Calculates available 1-hour time slots for a doctor on a specific date.
# It looks at the doctor's shift hours and subtracts any active appointments.
# 1. Get the doctor's shift times (safely handling dicts or objects)
    if isinstance(doctor, dict):
        start_str = doctor.get('shift_start_time', '09:00')
        end_str = doctor.get('shift_end_time', '17:00')
        doc_id = doctor.get('user_id')
    else:
        start_str = getattr(doctor, 'shift_start_time', '09:00')
        end_str = getattr(doctor, 'shift_end_time', '17:00')
        doc_id = getattr(doctor, 'user_id')

# 2. Generate all possible hourly slots for the shift
    all_slots = []
    try:
        start_time = datetime.strptime(start_str, "%H:%M")
        end_time = datetime.strptime(end_str, "%H:%M")
        
        current_time = start_time
        while current_time < end_time:
            all_slots.append(current_time.strftime("%H:%M"))
            current_time += timedelta(hours=1)
    except ValueError:
        return []

    # 3. Remove slots already booked for this doctor on this date (P1-14 fix:
    booked_times = set()
    for appt in appointment_list:
        if isinstance(appt, dict):
            appt_doctor_id = appt.get('doctor_id')
            appt_date = appt.get('date')
            appt_time = appt.get('start_time')
            appt_status = appt.get('status')
        else:
            appt_doctor_id = getattr(appt, 'doctor_id', None)
            appt_date = getattr(appt, 'date', None)
            appt_time = getattr(appt, 'start_time', None)
            appt_status = getattr(appt, 'status', None)
        if appt_doctor_id == doc_id and appt_date == target_date and appt_status != "Cancelled":
            booked_times.add(appt_time)

    return [slot for slot in all_slots if slot not in booked_times]
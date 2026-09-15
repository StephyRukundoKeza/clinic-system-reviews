print("Day one on clinic appointment system!")
import random
from datetime import datetime, timedelta


def generate_new_id_admin():
    # Generates a unique 8-digit ID for new admins.
    print("Generating your admin id")
    id=random.randrange(00000000,99999999)
    print(f"Your admin id is A-{id}")
    return f"A-{id}"

def generate_new_id_patient():
    # Generates a unique 8-digit ID for new patients.
    print("Generating your patients id")
    id=random.randrange(00000000,99999999)
    print(f"Your patient id is P-{id}")
    return f"P-{id}"

def generate_new_id_doctor():
    # Generates a unique 8-digit ID for new doctors.
    print("Generating your doctors id")
    id=random.randrange(00000000,99999999)
    print(f"Your doctor id is DR-{id}")
    return f"DR-{id}"

def generate_new_id_appointment():
# Generates a unique 6-digit ID for new appointments.
    id = random.randrange(100000, 999999)
    return f"APT-{id}"

def find_record_by_id(record_list, search_id):
    for record in record_list:
# Check if the record is a dictionary (freshly loaded from JSON by data_manager)
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



    pass
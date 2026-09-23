import random
from datetime import datetime, timedelta
import data_manager

def generate_new_id_admin():
    # Generates a unique 8-digit ID for new admins.
    print("Generating your admin id")
    id=random.randrange(10000000,99999999)
    print(f"Your admin id is A-{id}")
    return f"A-{id}"

def generate_new_id_patient(patients):
    
    while True:
    # Generates a unique 8-digit ID for new patients.
        print("Generating your patients id")
        id=random.randrange(10000000,99999999)
        new_id= f"P-{id}"
#checks for any duplicates
        for patient in patients:
            if isinstance(patient,dict):
                existing_id=patient["user_id"]
            else:
                existing_id=patient.user_id
                
            if existing_id == new_id:
                break
        else:
            print(f"Your patient id is P-{id}")
            return new_id

def generate_new_id_doctor(doctors):
    # Generates a unique 8-digit ID for new doctors.
    print("Generating your doctors id")
    id=random.randrange(10000000,99999999)
    new_id=f"DR-{id}"
    
    
    #checks for any duplicates
    for doctor in doctors:
        if isinstance(doctor,dict):
            existing_id=doctor["user_id"]
        else:
            existing_id=doctor.user_id
        if existing_id == new_id:
            break               
    else:
        print(f"Your doctor id is DR-{id}")
        return new_id

def generate_new_id_appointment(appointments):
    # Generates a unique 8-digit ID for new appointments.
    while True:
        id = random.randrange(10000000, 99999999)
        new_id = f"APT-{id}"
        
        # checks for any duplicates safely
        for appointment in appointments:
            # Safely get the ID whether it's an old JSON dictionary or a new OOP Object
            existing_id = appointment.get("appointment_id") if isinstance(appointment, dict) else getattr(appointment, 'appointment_id', None)
            
            if existing_id == new_id:
                break # Duplicate found, break the for-loop and generate a new random number
        else:
            # FIXED: Changed "DR-" to "APT-"
            print(f"Your appointment ID is {new_id}")
            return new_id



def generate_new_id(role, existing_users):
    # Generates the next sequential ID for a role instead of a random one,
    # so two new records can never end up with the same ID.
    prefixes = {"Patient": "P-", "Doctor": "DR-", "Admin": "A-"}
    prefix = prefixes.get(role)
    if prefix is None:
        raise ValueError(f"Unknown role '{role}'. Expected one of: {list(prefixes.keys())}")

    highest_number = 0
    for user in existing_users:
        existing_id = user.get('user_id') if isinstance(user, dict) else getattr(user, 'user_id', None)
        if existing_id and existing_id.startswith(prefix):
            number_part = existing_id[len(prefix):]
            if number_part.isdigit():
                highest_number = max(highest_number, int(number_part))

    new_id = f"{prefix}{highest_number + 1:08d}"
    print(f"Your {role.lower()} id is {new_id}")
    return new_id

def find_record_by_id(saved_data, search_id):
    for record in saved_data:
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

def get_available_time_slots(selected_doctor, appointment_date, appointments):
    # 1. Safely get the doctor's shift times and ID (handles both dicts and objects)
    shift_start = selected_doctor.get('shift_start_time') if isinstance(selected_doctor, dict) else selected_doctor.shift_start_time
    shift_end = selected_doctor.get('shift_end_time') if isinstance(selected_doctor, dict) else selected_doctor.shift_end_time
    doc_id = selected_doctor.get('user_id') if isinstance(selected_doctor, dict) else selected_doctor.user_id
    
    start_time = datetime.strptime(shift_start, "%H:%M")
    end_time = datetime.strptime(shift_end, "%H:%M")
    
    # 2. Find any times already booked for this doctor on this date
    booked_slots = []
    for appointment in appointments:
        # Safely check if the appointment is a dict or object, and look for doctor_id (NOT user_id)
        appointment_doctor_id = (appointment.get('doctor_id') if isinstance(appointment, dict)
                else getattr(appointment, 'doctor_id', None))
        appointment_date_value = appointment.get('date') if isinstance(appointment, dict) else getattr(appointment, 'date', getattr(appointment, 'appointment_date', None))
        appointment_start = appointment.get('start_time') if isinstance(appointment, dict) else appointment.start_time
        
        # If the doctor is booked on this exact date, save the start time to our booked list
        if appointment_doctor_id == doc_id and appointment_date_value == appointment_date:
            booked_slots.append(appointment_start)
                                
    # 3. Calculate free 1-hour slots
    available_slots = []
    current_time = start_time
    
    while current_time + timedelta(minutes=60) <= end_time:
        start = current_time.strftime("%H:%M")
        end = (current_time + timedelta(minutes=60)).strftime("%H:%M")
        
        # Only add the slot if it is NOT in our booked list
        if start not in booked_slots:
            available_slots.append(f"{start} - {end}")
            
        current_time += timedelta(minutes=60)
            
    # 4. Print them out nicely so the patient can see them
    for position, slot in enumerate(available_slots, start=1):
        print(f"{position}. {slot}")
            
    # 5. CRITICAL: Return the list back to sub_main so the menu knows slots exist!
    return available_slots

    


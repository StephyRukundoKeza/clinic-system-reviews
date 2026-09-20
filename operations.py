import random
from datetime import datetime, timedelta
import data_manager

def generate_new_id_admin():
    # Generates a unique 8-digit ID for new admins.
    print("Generating your admin id")
    id=random.randrange(00000000,99999999)
    print(f"Your admin id is A-{id}")
    return f"A-{id}"

def generate_new_id_patient(patients):
    
    while True:
    # Generates a unique 8-digit ID for new patients.
        print("Generating your patients id")
        id=random.randrange(00000000,99999999)
        new_id= f"P-{id}"
#checks for any duplicates
        for patient in patients:
            if patient["user_id"] ==new_id:
                break
        else:
            print(f"Your patient id is P-{id}")
            return new_id

def generate_new_id_doctor(doctors):
    # Generates a unique 8-digit ID for new doctors.
    print("Generating your doctors id")
    id=random.randrange(00000000,99999999)
    new_id=f"DR-{id}"
    
    
    #checks for any duplicates
    for doctor in doctors:
        if doctor["user_id"] ==new_id:
                break
    else:
        print(f"Your doctor id is DR-{id}")
        return new_id

def generate_new_id_appointment(appointments):
# Generates a unique 6-digit ID for new appointments.
    id = random.randrange(100000, 999999)
    new_id=f"APT-{id}"
    
    #checks for any duplicates
    for appointment in appointments:
        if appointment["appointment_id"] ==new_id:
                    break
    else:
        print(f"Your appointment id is DR-{id}")
        return  new_id



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

def get_available_time_slots(selected_doctor , appointment_date, appointments):
# Calculates available 1-hour time slots for a doctor on a specific date.
# It looks at the doctor's shift hours and subtracts any active appointments.
# 1. Get the doctor's shift times (safely handling dicts or objects)
    
    
    all_slots=[]
    start_time = datetime.strptime(selected_doctor['shift_start_time'],"%H:%M")
    end_time = datetime.strptime(selected_doctor['shift_end_time'],"%H:%M")
    doc_id = selected_doctor["user_id"]
    booked_slots=[]  
        
    for appointment in appointments:
        if(appointment["doctor_id"] == doc_id
            and appointment['date'] == appointment_date):
            booked_slots.append(appointment["start_time"])          
                    
    available_slots = []
    current_time=start_time
    while current_time + timedelta(minutes=60) <= end_time:

        start = current_time.strftime("%H:%M")
        end = (current_time + timedelta(minutes=60)).strftime("%H:%M")

        if start not in booked_slots: 
            available_slots.append(f"{start} - {end}")

        current_time += timedelta(minutes=60)
        
    for position, slot in enumerate(available_slots, start=1):
        print(f"{position}.{slot}")

    
            

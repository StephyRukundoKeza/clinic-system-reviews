# sub_main.py
# This file will contain the helper functions to run the main.py file.

import models
import validation
import operations
import random

# 1st menu for all patients to register

def patient_self_registration_menu(patients):
    first = validation.get_valid_firstname()
    last = validation.get_valid_lastname()
    name = f"{first} {last}"

    dob = validation.get_valid_birthdate()
    gender = input("Enter your gender (e.g., Male/Female): ").strip()
    phone = validation.get_valid_phone_number()
    email = validation.get_valid_email()
    address = input("Enter your physical address: ").strip()
    new_id = operations.generate_new_id_patient(patients)
    new_pin = str(random.randint(1000, 9999)) # Create a random 4-digit PIN for the patient

    new_patient = models.Patient(new_id, name, new_pin, phone, gender, str(dob), email, address)
    patients.append(new_patient)
    print(f"\nRegistration successful!")
    print(f"Your patient ID is {new_id} and your PIN is {new_pin}.")
    print("\nPlease use these credentials to login.")


# Administrator menu

def create_admin_account(admins):
    print("\n---Create New Admin Account---")
    first = validation.get_valid_firstname()
    last = validation.get_valid_lastname()
    name = f"{first} {last}"

    phone = validation.get_valid_phone_number()
    pin = input("Create a 4-digit PIN for the admin: ").strip()

    new_id = operations.generate_new_id_admin()
    new_admin = models.Admin(new_id, name, pin, phone)
    admins.append(new_admin)

    print(f"\nSuccessful! Admin {name} created with ID: {new_id}")

def delete_admin_account(admins):
    print("\n---Delete Admin Account---")
    search_id = input("Enter the admin ID to delete(e.g., A-12345678): ").strip().upper()
    
    a = operations.find_record_by_id(admins, search_id)
    
    if not a:
        print("Error: Admin not found. Please check the ID.")
        return

    print("\nAdmin Found:")
    if isinstance(a, dict):
        print(f"ID: {a.get('user_id')} | Name: {a.get('name')} | Phone: {a.get('phone_number')}")
    else:
        print(f"ID: {a.user_id} | Name: {a.name} | Phone: {a.phone_number}")

    confirmation = input(f"Are you sure you want to delete Admin {search_id}? (yes/no): ").strip().lower()
    if confirmation == "yes":
        admins.remove(a)
        print(f"Admin {search_id} has been deleted successfully.")
    else:
        print("Attempt Cancelled.") 


def admin_register_patient(patients):
    print("\n---Register New Patient (Admin)---")
    first = validation.get_valid_firstname()
    last = validation.get_valid_lastname()
    name = f"{first} {last}"

    dob = validation.get_valid_birthdate()
    gender = input("Enter your gender (e.g., Male/Female): ").strip()
    phone = validation.get_valid_phone_number()
    email = validation.get_valid_email()
    address = input("Enter your physical address: ").strip()
    pin = input("Create a 4-digit PIN for the patient: ").strip()
    
    new_id = operations.generate_new_id_patient(patients)
    new_patient = models.Patient(new_id, name, pin, phone, gender, str(dob), email, address)
    patients.append(new_patient)
    
    print(f"\nSuccessful! Patient {name} registered with ID: {new_id}")

def admin_display_patients(patients):
    print("\n---Display All Registered Patients (Admin)---")
    if not patients:
        print("No patients registered yet.")
        return

    print("\nRegistered Patients:")
    for p in patients:
        if isinstance(p, dict):
            print(f"ID: {p.get('user_id')} | Name: {p.get('name')} | Phone: {p.get('phone_number')}")
        else:
            print(f"ID: {p.user_id} | Name: {p.name} | Phone: {p.phone_number}")

def admin_search_patient(patients):
    print("---Search Patient (Admin)---")
    search_id = input("Enter the patient ID to search(e. g., P-12345678): ").strip().upper()
    
    p = operations.find_record_by_id(patients, search_id)
    
    if not p:
        print("Error: Patient not found. Please check the ID.")
        return
        
    print("\nPatient Found:")
    if isinstance(p, dict):
        print(f"ID: {p.get('user_id')} | Name: {p.get('name')} | Phone: {p.get('phone_number')}")
    else:
        print(f"ID: {p.user_id} | Name: {p.name} | Phone: {p.phone_number}")

def admin_update_patient(patients):
    print("\n---Update Patient Profile (Admin)---")
    search_id = input("Enter the patient ID to update(e.g., P-12345678): ").strip().upper()
    
    p = operations.find_record_by_id(patients, search_id)
    
    if not p:
        print("Error: Patient not found. Please check the ID.")
        return

    print("\nPatient Found:")
    if isinstance(p, dict):
        print(f"ID: {p.get('user_id')} | Name: {p.get('name')} | Phone: {p.get('phone_number')}")
    else:
        print(f"ID: {p.user_id} | Name: {p.name} | Phone: {p.phone_number}")

    print("\nEnter new details (leave blank to keep current value):")
    new_name = input("New Name: ").strip()
    new_phone = input("New Phone: ").strip()
    new_gender = input("New Gender (e.g., Male/Female): ").strip()
    new_dob = input("New DOB (YYYY-MM-DD): ").strip()
    new_email = input("New Email: ").strip()
    new_address = input("New Address: ").strip()
    
    # We still have to check type here because we are modifying the data
    if isinstance(p, dict):
        if new_name: p['name'] = new_name
        if new_phone: p['phone_number'] = new_phone
        if new_gender: p['gender'] = new_gender
        if new_dob: p['date_of_birth'] = str(new_dob)
        if new_email: p['email'] = new_email
        if new_address: p['address'] = new_address
    else:
        p.update_profile(name=new_name, phone_number=new_phone, gender=new_gender, date_of_birth=str(new_dob), email=new_email, address=new_address)
    print("\nPatient profile updated successfully.")

def admin_delete_patient(patients):
    print("\n---Delete Patient Profile (Admin)---")
    search_id = input("Enter the patient ID to delete(e.g., P-12345678): ").strip().upper()
    
    p = operations.find_record_by_id(patients, search_id)
    
    if not p:
        print("Error: Patient not found. Please check the ID.")
        return

    print("\nPatient Found:")
    if isinstance(p, dict):
        print(f"ID: {p.get('user_id')} | Name: {p.get('name')} | Phone: {p.get('phone_number')}")
    else:
        print(f"ID: {p.user_id} | Name: {p.name} | Phone: {p.phone_number}")

    confirmation = input(f"Are you sure you want to delete Patient {search_id}? (yes/no): ").strip().lower()
    if confirmation == "yes":
        patients.remove(p)
        print(f"Patient {search_id} has been deleted successfully.")
    else:
        print("Attempt Cancelled.") 

def admin_add_doctor(doctors):
    print("\n---Add New Doctor (Admin)---")
    first = validation.get_valid_firstname()
    last = validation.get_valid_lastname()
    name = f"{first} {last}"

    specialization = input("Enter the doctor's specialization: ").strip()
    shift_start_time = input("Enter the doctor's shift start time (HH:MM): ").strip()
    shift_end_time = input("Enter the doctor's shift end time (HH:MM): ").strip()
    phone = validation.get_valid_phone_number()
    pin = input("Create a 4-digit PIN for the doctor: ").strip()

    new_id = operations.generate_new_id_doctor()
    new_doctor = models.Doctor(new_id, name, pin, phone, specialization, shift_start_time, shift_end_time)
    doctors.append(new_doctor)

    print(f"\nSuccessful! Doctor {name} added with ID: {new_id}")

def admin_display_doctors(doctors):
    print("\n---Display All Registered Doctors (Admin)---")
    if not doctors:
        print("No doctors registered yet.")
        return

    print("\nRegistered Doctors:")
    for d in doctors:
        if isinstance(d, dict):
            print(f"ID: {d.get('user_id')} | Name: {d.get('name')} | Specialization: {d.get('specialization')}")
        else:
            print(f"ID: {d.user_id} | Name: {d.name} | Specialization: {d.specialization}")

def admin_search_doctor(doctors):
    print("\n---Search Doctor (Admin)---")
    search_id = input("Enter the doctor ID to search(e.g., DR-12345678): ").strip().upper()
    
    d = operations.find_record_by_id(doctors, search_id)
    
    if not d:
        print("Error: Doctor not found. Please check the ID.")
        return
        
    print("\nDoctor Found:")
    if isinstance(d, dict):
        print(f"ID: {d.get('user_id')} | Name: {d.get('name')} | Specialization: {d.get('specialization')}")
    else:
        print(f"ID: {d.user_id} | Name: {d.name} | Specialization: {d.specialization}")

def admin_update_doctor(doctors):
    print("---Update Doctor Profile (Admin)---")
    search_id = input("Enter the doctor ID to update(e.g., DR-12345678): ").strip().upper()
    
    d = operations.find_record_by_id(doctors, search_id)
    
    if not d:
        print("Error: Doctor not found. Please check the ID.")
        return

    print("\nDoctor Found:")
    if isinstance(d, dict):
        print(f"ID: {d.get('user_id')} | Name: {d.get('name')} | Specialization: {d.get('specialization')}")
    else:
        print(f"ID: {d.user_id} | Name: {d.name} | Specialization: {d.specialization}")

    print("\nEnter new details (leave blank to keep current value):")
    new_name = input("New Name: ").strip()
    new_specialization = input("New Specialization: ").strip()
    new_shift_start_time = input("New Shift Start Time (HH:MM): ").strip()
    new_shift_end_time = input("New Shift End Time (HH:MM): ").strip()
    
    if isinstance(d, dict):
        if new_name: d['name'] = new_name
        if new_specialization: d['specialization'] = new_specialization
        if new_shift_start_time: d['shift_start_time'] = new_shift_start_time
        if new_shift_end_time: d['shift_end_time'] = new_shift_end_time
    else:
        if new_shift_start_time and new_shift_end_time:
            d.update_shifts(new_shift_start_time, new_shift_end_time)
        if new_name:
            setattr(d, 'name', new_name)
    print("\nDoctor profile updated successfully.")

def admin_delete_doctor(doctors):
    print("---Delete Doctor Profile (Admin)---")
    search_id = input("Enter the doctor ID to delete(e.g., DR-12345678): ").strip().upper()
    
    d = operations.find_record_by_id(doctors, search_id)
    
    if not d:
        print("Error: Doctor not found. Please check the ID.")
        return

    print("\nDoctor Found:")
    if isinstance(d, dict):
        print(f"ID: {d.get('user_id')} | Name: {d.get('name')} | Specialization: {d.get('specialization')}")
    else:
        print(f"ID: {d.user_id} | Name: {d.name} | Specialization: {d.specialization}")

    confirmation = input(f"Are you sure you want to delete Doctor {search_id}? (yes/no): ").strip().lower()
    if confirmation == "yes":
        doctors.remove(d)
        print(f"Doctor {search_id} has been deleted successfully.")
    else:
        print("Attempt Cancelled.")

def admin_view_appointments(appointments):
    print("---View All Appointments (Admin)---")
    if not appointments:
        print("No appointments scheduled yet.")
        return

    print("\nScheduled Appointments:")
    for a in appointments:
        if isinstance(a, dict):
            print(f"Appointment ID: {a.get('appointment_id')} | Patient ID: {a.get('patient_id')} | Doctor ID: {a.get('doctor_id')} | Date: {a.get('appointment_date')}")
        else:
            print(f"Appointment ID: {a.appointment_id} | Patient ID: {a.patient_id} | Doctor ID: {a.doctor_id} | Date: {a.appointment_date}")

def admin_cancel_appointment(appointments):
    print("---Cancel Appointment (Admin)---")
    search_id = input("Enter the appointment ID to cancel: ").strip().upper()
    found = False

    for a in appointments:
        if isinstance(a, dict):
            if a.get('appointment_id') == search_id:
                print("\nAppointment Found:")
                print(f"Appointment ID: {a.get('appointment_id')} | Patient ID: {a.get('patient_id')} | Doctor ID: {a.get('doctor_id')} | Date: {a.get('appointment_date')}")
                found = True
                break
        else:
            if a.appointment_id == search_id:
                print("\nAppointment Found:")
                print(f"Appointment ID: {a.appointment_id} | Patient ID: {a.patient_id} | Doctor ID: {a.doctor_id} | Date: {a.appointment_date}")
                found = True
                break

    if not found:
        print("Error: Appointment not found. Please check the ID.")
        return

    # If we found the appointment, proceed to cancel it
    confirmation = input(f"Are you sure you want to cancel Appointment {search_id}? (yes/no): ").strip().lower()
    if confirmation == "yes":
        appointments.remove(a)
        print(f"Appointment {search_id} has been cancelled successfully.")
    else:
        print("Attempt Cancelled.")

# Patient menu

def patient_view_information(current_patients):
    print("\n---View My Information---")
    if isinstance(current_patients, dict):
        print(f"Patient ID : {current_patients.get('user_id')}")
        print(f"Name       : {current_patients.get('name')}")
        print(f"DOB        : {current_patients.get('date_of_birth')}")
        print(f"Gender     : {current_patients.get('gender')}")
        print(f"Phone      : {current_patients.get('phone_number')}")
        print(f"Email      : {current_patients.get('email')}")
        print(f"Address    : {current_patients.get('address')}")
    else:
        print(f"Patient ID : {current_patients.user_id}")
        print(f"Name       : {current_patients.name}")
        print(f"DOB        : {getattr(current_patients, 'date_of_birth', getattr(current_patients, 'dob', 'N/A'))}")
        print(f"Gender     : {current_patients.gender}")
        print(f"Phone      : {current_patients.phone_number}")
        print(f"Email      : {current_patients.email}")
        print(f"Address    : {current_patients.address}")
     
def patient_book_appointment(current_patients, doctors, appointments):
    print("\n--- Book an Appointment ---")
    if not doctors:
        print("No doctors available in the system yet.")
        return

    # Extract patient ID safely
    patient_id = current_patients.get('user_id') if isinstance(current_patients, dict) else current_patients.user_id

    # 1. Display available doctors
    print("\nAvailable Doctors:")
    for d in doctors:
        if isinstance(d, dict):
            print(f"ID: {d.get('user_id')} | Name: Dr. {d.get('name')} | Specialization: {d.get('specialization')}")
            print(f"    Working hours: {d.get('shift_start_time')} - {d.get('shift_end_time')}")
        else:
            print(f"ID: {d.user_id} | Name: Dr. {d.name} | Specialization: {d.specialization}")
            # Handle slight attribute name variations between team members
            start = getattr(d, 'shift_start_time', getattr(d, 'shift_start', '09:00'))
            end = getattr(d, 'shift_end_time', getattr(d, 'shift_end', '17:00'))
            print(f"    Working hours: {start} - {end}")

    doc_id = input("\nEnter the Doctor ID you wish to see (e.g., DR-12345678): ").strip().upper()
    doctor = operations.find_record_by_id(doctors, doc_id)

    if not doctor:
        print("Error: Doctor not found.")
        return

    doc_name = doctor.get('name') if isinstance(doctor, dict) else doctor.name
    print(f"\nYou selected: Dr. {doc_name}")

    # 2. Get target date using validation
    target_date = validation.get_valid_appointment_date()

    # 3. Use operations helper to find free slots
    available_slots = operations.get_available_time_slots(doctor, str(target_date), appointments)

    if not available_slots:
        print(f"Sorry, Dr. {doc_name} has no open slots on {target_date}.")
        return

    print(f"\nAvailable time slots for {target_date}:")
    for idx, slot in enumerate(available_slots, 1):
        print(f"  [{idx}] {slot}")

    slot_choice = validation.get_integer("Select slot number: ", min_val=1, max_val=len(available_slots))
    selected_time = available_slots[slot_choice - 1]

    # 4. Generate unique ID and create the Appointment
    new_apt_id = operations.generate_new_id_appointment()
    
    new_apt = models.Appointment(
        appointment_id=new_apt_id,
        patient_id=patient_id,
        doctor_id=doc_id,
        date=str(target_date),
        start_time=selected_time,
        status="Active"
    )
    appointments.append(new_apt)

    print(f"\nSuccess! Appointment booked.")
    print(f"Appointment ID: {new_apt_id} | Date: {target_date} | Time: {selected_time}")


def patient_view_appointments(current_patients, appointments):
    print("\n--- My Appointments ---")
    patient_id = current_patients.get('user_id') if isinstance(current_patients, dict) else current_patients.user_id

    my_appointments = []
    for a in appointments:
        apt_patient = a.get('patient_id') if isinstance(a, dict) else getattr(a, 'patient_id', None)
        if apt_patient == patient_id:
            my_appointments.append(a)

    if not my_appointments:
        print("You have no scheduled appointments.")
        return

    print("\n---------------------------------------------------------------------------------------------")
    print(f"{'Appointment ID':<12} | {'Doctor ID':<12} | {'Date':<12} | {'Time':<8} | {'Status':<10}")
    print("---------------------------------------------------------------------------------------------")
    for a in my_appointments:
        if isinstance(a, dict):
            print(f"{a.get('appointment_id'):<12} | {a.get('doctor_id'):<12} | {a.get('date', a.get('appointment_date')):<12} | {a.get('start_time'):<8} | {a.get('status'):<10}")
        else:
            date_val = getattr(a, 'date', getattr(a, 'appointment_date', 'N/A'))
            print(f"{a.appointment_id:<12} | {a.doctor_id:<12} | {date_val:<12} | {a.start_time:<8} | {a.status:<10}")
    print("---------------------------------------------------------------------------------------------")


def patient_cancel_appointment(current_patients, appointments):
    print("\n--- Cancel My Appointment ---")
    patient_id = current_patients.get('user_id') if isinstance(current_patients, dict) else current_patients.user_id

    search_id = input("Enter the Appointment ID to cancel (e.g., APT-123456): ").strip().upper()
    apt = operations.find_record_by_id(appointments, search_id)

    if not apt:
        print("Error: Appointment not found.")
        return

    apt_patient_id = apt.get('patient_id') if isinstance(apt, dict) else getattr(apt, 'patient_id', None)
    if apt_patient_id != patient_id:
        print("Error: Appointment not found.")
        return

    confirm = input(f"Are you sure you want to cancel appointment {search_id}? (Y/N): ").strip().upper()
    if confirm == 'Y' or confirm == 'YES':
        if isinstance(apt, dict):
            apt['status'] = 'Cancelled'
        else:
            if hasattr(apt, 'update_status'):
                apt.update_status('Cancelled')
            else:
                setattr(apt, 'status', 'Cancelled')
        print(f"Appointment {search_id} has been cancelled.")
    else:
        print("Cancellation aborted.")


# Doctor menu

def doctor_view_schedule(current_doctors, appointments, patients=None):
# Displays all appointments associated with the logged-in doctor.
#Handles both dictionary and object representations cleanly.
    print("\n--- My Appointment Schedule ---")
    
    # Extract Doctor ID safely
    doc_id = current_doctors.get('user_id') if isinstance(current_doctors, dict) else getattr(current_doctors, 'user_id', None)

    # Filter appointments for this doctor
    doctor_appointments = []
    for a in appointments:
        apt_doc = a.get('doctor_id') if isinstance(a, dict) else getattr(a, 'doctor_id', None)
        if apt_doc == doc_id:
            doctor_appointments.append(a)

    if not doctor_appointments:
        print("You have no scheduled appointments on record.")
        return

    print("\n---------------------------------------------------------------------------------------------")
    print(f"{'Appointment ID':<15} | {'Patient ID':<12} | {'Date':<12} | {'Time':<8} | {'Status':<10}")
    print("---------------------------------------------------------------------------------------------")

    for a in doctor_appointments:
        if isinstance(a, dict):
            apt_id = a.get('appointment_id', 'N/A')
            p_id = a.get('patient_id', 'N/A')
            date = a.get('date') or a.get('appointment_date', 'N/A')
            time = a.get('start_time', 'N/A')
            status = a.get('status', 'Active')
        else:
            apt_id = getattr(a, 'appointment_id', 'N/A')
            p_id = getattr(a, 'patient_id', 'N/A')
            date = getattr(a, 'date', getattr(a, 'appointment_date', 'N/A'))
            time = getattr(a, 'start_time', 'N/A')
            status = getattr(a, 'status', 'Active')

        print(f"{apt_id:<12} | {p_id:<12} | {date:<12} | {time:<8} | {status:<10}")
    print("---------------------------------------------------------------------------------------------\n")

def doctor_update_appointment_status(current_doctors, appointments):
    #Allows the doctor to update the status of an appointment assigned to them.
    print("\n--- Update Appointment Status ---")
    doc_id = current_doctors.get('user_id') if isinstance(current_doctors, dict) else getattr(current_doctors, 'user_id', None)

    apt_id = input("Enter the Appointment ID to update (e.g., APT-123456): ").strip().upper()
    apt = operations.find_record_by_id(appointments, apt_id)
    if not apt:
        print("Error: Appointment not found.")
        return

    # Verify ownership
    apt_doc_id = apt.get('doctor_id') if isinstance(apt, dict) else getattr(apt, 'doctor_id', None)
    if apt_doc_id != doc_id:
        print("Error: You can only update appointments assigned to you.")
        return

    print("\n--- Select New Status ---")
    print("1. Completed")
    print("2. In-Progress")
    print("3. Cancelled")
    print("4. Active")

    choice = validation.get_integer("Enter choice (1-4): ", min_val=1, max_val=4)
    status_map = {1: "Completed", 2: "In-Progress", 3: "Cancelled", 4: "Active"}
    new_status = status_map[choice]

    if isinstance(apt, dict):
        apt['status'] = new_status
    else:
        if hasattr(apt, 'update_status'):
            apt.update_status(new_status)
        else:
            setattr(apt, 'status', new_status)

    print(f"\nSuccess: Appointment {apt_id} status updated to '{new_status}'.")


def doctor_view_profile(current_doctor):
# Displays profile details for the currently logged-in doctor.
    print("\n--- My Profile ---")
    if isinstance(current_doctor, dict):
        print(f"Doctor ID    : {current_doctor.get('user_id')}")
        print(f"Name         : Dr. {current_doctor.get('name')}")
        print(f"Specialty    : {current_doctor.get('specialization', 'General')}")
        print(f"Phone        : {current_doctor.get('phone_number', 'N/A')}")
        print(f"Shift Start  : {current_doctor.get('shift_start_time', '09:00')}")
        print(f"Shift End    : {current_doctor.get('shift_end_time', '17:00')}")
    else:
        print(f"Doctor ID    : {getattr(current_doctor, 'user_id', 'N/A')}")
        print(f"Name         : Dr. {getattr(current_doctor, 'name', 'N/A')}")
        print(f"Specialty    : {getattr(current_doctor, 'specialization', 'General')}")
        print(f"Phone        : {getattr(current_doctor, 'phone_number', 'N/A')}")
        print(f"Shift Start  : {getattr(current_doctor, 'shift_start_time', getattr(current_doctor, 'shift_start', '09:00'))}")
        print(f"Shift End    : {getattr(current_doctor, 'shift_end_time', getattr(current_doctor, 'shift_end', '17:00'))}")

def doctor_update_shift(current_doctor):
# Allows the doctor to change their shift hours.
    print("\n--- Update Shift Working Hours ---")
    new_start = validation.get_valid_time("Enter new Shift Start Time (HH:MM in 24h format): ")
    new_end = validation.get_valid_time("Enter new Shift End Time (HH:MM in 24h format): ")

    if isinstance(current_doctor, dict):
        current_doctor['shift_start_time'] = new_start
        current_doctor['shift_end_time'] = new_end
    else:
        if hasattr(current_doctor, 'update_shifts'):
            current_doctor.update_shifts(new_start, new_end)
        elif hasattr(current_doctor, 'update_shift'):
            current_doctor.update_shift(new_start, new_end)
        else:
            setattr(current_doctor, 'shift_start_time', new_start)
            setattr(current_doctor, 'shift_end_time', new_end)

    print(f"\nShift updated successfully: {new_start} - {new_end}")
    
    
    
    

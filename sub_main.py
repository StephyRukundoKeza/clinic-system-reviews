# submain.py
# This file will contain the helper functions to run the main.py file.

import models
import validation
import operations
import random

# 1st menu for all patients to register

def patient_self_registration_menu(patient_list):
    first = validation.get_valid_firstname()
    last = validation.get_valid_lastname()
    name = f"{first} {last}"

    dob = validation.get_valid_birthdate()
    gender = input("Enter your gender (e.g., Male/Female): ").strip()
    phone = validation.get_valid_phone_number()
    email = validation.get_valid_email()
    address = input("Enter your physical address: ").strip()
    new_id = operations.generate_new_id_patient()
    new_pin = str(random.randint(1000, 9999)) # Create a random 4-digit PIN for the patient

    new_patient = models.Patient(new_id, name, new_pin, phone, gender, str(dob), email, address)
    patient_list.append(new_patient)
    print(f"\nRegistration successful!")
    print(f"Your patient ID is {new_id} and your PIN is {new_pin}.")
    print("\nPlease use these credentials to login.")


# Administrator menu

def create_admin_account(admin_list):
    print("---Create New Admin Account---")
    first = validation.get_valid_firstname()
    last = validation.get_valid_lastname()
    name = f"{first} {last}"

    phone = validation.get_valid_phone_number()
    pin = input("Create a 4-digit PIN for the admin: ").strip()

    new_id = operations.generate_new_id_admin()
    new_admin = models.Admin(new_id, name, pin, phone)
    admin_list.append(new_admin)

    print(f"\nSuccessful! Admin {name} created with ID: {new_id}")

def delete_admin_account(admin_list):
    print("---Delete Admin Account---")
    search_id = input("Enter the admin ID to delete(e.g., A-12345678): ").strip().upper()
    
    a = operations.find_record_by_id(admin_list, search_id)
    
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
        admin_list.remove(a)
        print(f"Admin {search_id} has been deleted successfully.")
    else:
        print("Attempt Cancelled.") 


def admin_register_patient(patient_list):
    print("---Register New Patient (Admin)---")
    first = validation.get_valid_firstname()
    last = validation.get_valid_lastname()
    name = f"{first} {last}"

    dob = validation.get_valid_birthdate()
    gender = input("Enter your gender (e.g., Male/Female): ").strip()
    phone = validation.get_valid_phone_number()
    email = validation.get_valid_email()
    address = input("Enter your physical address: ").strip()
    pin = input("Create a 4-digit PIN for the patient: ").strip()
    
    new_id = operations.generate_new_id_patient()
    new_patient = models.Patient(new_id, name, pin, phone, gender, str(dob), email, address)
    patient_list.append(new_patient)
    
    print(f"\nSuccessful! Patient {name} registered with ID: {new_id}")

def admin_display_patients(patient_list):
    print("---Display All Registered Patients (Admin)---")
    if not patient_list:
        print("No patients registered yet.")
        return

    print("\nRegistered Patients:")
    for p in patient_list:
        if isinstance(p, dict):
            print(f"ID: {p.get('user_id')} | Name: {p.get('name')} | Phone: {p.get('phone_number')}")
        else:
            print(f"ID: {p.user_id} | Name: {p.name} | Phone: {p.phone_number}")

def admin_search_patient(patient_list):
    print("---Search Patient (Admin)---")
    search_id = input("Enter the patient ID to search(e.g., P-12345678): ").strip().upper()
    
    p = operations.find_record_by_id(patient_list, search_id)
    
    if not p:
        print("Error: Patient not found. Please check the ID.")
        return
        
    print("\nPatient Found:")
    if isinstance(p, dict):
        print(f"ID: {p.get('user_id')} | Name: {p.get('name')} | Phone: {p.get('phone_number')}")
    else:
        print(f"ID: {p.user_id} | Name: {p.name} | Phone: {p.phone_number}")

def admin_update_patient(patient_list):
    print("---Update Patient Profile (Admin)---")
    search_id = input("Enter the patient ID to update(e.g., P-12345678): ").strip().upper()
    
    p = operations.find_record_by_id(patient_list, search_id)
    
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

def admin_delete_patient(patient_list):
    print("---Delete Patient Profile (Admin)---")
    search_id = input("Enter the patient ID to delete(e.g., P-12345678): ").strip().upper()
    
    p = operations.find_record_by_id(patient_list, search_id)
    
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
        patient_list.remove(p)
        print(f"Patient {search_id} has been deleted successfully.")
    else:
        print("Attempt Cancelled.") 

def admin_add_doctor(doctor_list):
    print("---Add New Doctor (Admin)---")
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
    doctor_list.append(new_doctor)

    print(f"\nSuccessful! Doctor {name} added with ID: {new_id}")

def admin_display_doctors(doctor_list):
    print("---Display All Registered Doctors (Admin)---")
    if not doctor_list:
        print("No doctors registered yet.")
        return

    print("\nRegistered Doctors:")
    for d in doctor_list:
        if isinstance(d, dict):
            print(f"ID: {d.get('user_id')} | Name: {d.get('name')} | Specialization: {d.get('specialization')}")
        else:
            print(f"ID: {d.user_id} | Name: {d.name} | Specialization: {d.specialization}")

def admin_search_doctor(doctor_list):
    print("---Search Doctor (Admin)---")
    search_id = input("Enter the doctor ID to search(e.g., DR-12345678): ").strip().upper()
    
    d = operations.find_record_by_id(doctor_list, search_id)
    
    if not d:
        print("Error: Doctor not found. Please check the ID.")
        return
        
    print("\nDoctor Found:")
    if isinstance(d, dict):
        print(f"ID: {d.get('user_id')} | Name: {d.get('name')} | Specialization: {d.get('specialization')}")
    else:
        print(f"ID: {d.user_id} | Name: {d.name} | Specialization: {d.specialization}")

def admin_update_doctor(doctor_list):
    print("---Update Doctor Profile (Admin)---")
    search_id = input("Enter the doctor ID to update(e.g., DR-12345678): ").strip().upper()
    
    d = operations.find_record_by_id(doctor_list, search_id)
    
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

def admin_delete_doctor(doctor_list):
    print("---Delete Doctor Profile (Admin)---")
    search_id = input("Enter the doctor ID to delete(e.g., DR-12345678): ").strip().upper()
    
    d = operations.find_record_by_id(doctor_list, search_id)
    
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
        doctor_list.remove(d)
        print(f"Doctor {search_id} has been deleted successfully.")
    else:
        print("Attempt Cancelled.")

def admin_view_appointments(appointment_list):
    print("---View All Appointments (Admin)---")
    if not appointment_list:
        print("No appointments scheduled yet.")
        return

    print("\nScheduled Appointments:")
    for a in appointment_list:
        if isinstance(a, dict):
            print(f"Appointment ID: {a.get('appointment_id')} | Patient ID: {a.get('patient_id')} | Doctor ID: {a.get('doctor_id')} | Date: {a.get('date')}")
        else:
            print(f"Appointment ID: {a.appointment_id} | Patient ID: {a.patient_id} | Doctor ID: {a.doctor_id} | Date: {a.date}")

def admin_cancel_appointment(appointment_list):
    print("---Cancel Appointment (Admin)---")
    search_id = input("Enter the appointment ID to cancel: ").strip().upper()
    found = False

    for a in appointment_list:
        if isinstance(a, dict):
            if a.get('appointment_id') == search_id:
                print("\nAppointment Found:")
                print(f"Appointment ID: {a.get('appointment_id')} | Patient ID: {a.get('patient_id')} | Doctor ID: {a.get('doctor_id')} | Date: {a.get('date')}")
                found = True
                break
        else:
            if a.appointment_id == search_id:
                print("\nAppointment Found:")
                print(f"Appointment ID: {a.appointment_id} | Patient ID: {a.patient_id} | Doctor ID: {a.doctor_id} | Date: {a.date}")
                found = True
                break

    if not found:
        print("Error: Appointment not found. Please check the ID.")
        return

    # If we found the appointment, proceed to cancel it
    confirmation = input(f"Are you sure you want to cancel Appointment {search_id}? (yes/no): ").strip().lower()
    if confirmation == "yes":
        appointment_list.remove(a)
        print(f"Appointment {search_id} has been cancelled successfully.")
    else:
        print("Attempt Cancelled.")

def patient_view_information(patient):
    print("---View Patient Information---")
    if isinstance(patient, dict):
        print(f"ID: {patient.get('user_id')} | Name: {patient.get('name')} | Phone: {patient.get('phone_number')}")
        print(f"Gender: {patient.get('gender')} | DOB: {patient.get('date_of_birth')} | Email: {patient.get('email')}")
        print(f"Address: {patient.get('address')}")
    else:
        print(f"ID: {patient.user_id} | Name: {patient.name} | Phone: {patient.phone_number}")
        print(f"Gender: {patient.gender} | DOB: {patient.date_of_birth} | Email: {patient.email}")
        print(f"Address: {patient.address}")


def patient_view_own_appointments(patient, appointment_list):
    print("---View My Appointments---")
    patient_id = patient.get('user_id') if isinstance(patient, dict) else getattr(patient, 'user_id', None)
    found_any = False
    for a in appointment_list:
        appt_patient_id = a.get('patient_id') if isinstance(a, dict) else getattr(a, 'patient_id', None)
        if appt_patient_id == patient_id:
            found_any = True
            if isinstance(a, dict):
                print(f"Appointment ID: {a.get('appointment_id')} | Doctor ID: {a.get('doctor_id')} | Date: {a.get('date')} | Time: {a.get('start_time')} | Status: {a.get('status')}")
            else:
                print(f"Appointment ID: {a.appointment_id} | Doctor ID: {a.doctor_id} | Date: {a.date} | Time: {a.start_time} | Status: {a.status}")
    if not found_any:
        print("You have no appointments.")


def doctor_view_appointments(doctor, appointment_list):
    print("---View My Appointments (Doctor)---")
    doctor_id = doctor.get('user_id') if isinstance(doctor, dict) else getattr(doctor, 'user_id', None)
    found_any = False
    for a in appointment_list:
        appt_doctor_id = a.get('doctor_id') if isinstance(a, dict) else getattr(a, 'doctor_id', None)
        if appt_doctor_id == doctor_id:
            found_any = True
            if isinstance(a, dict):
                print(f"Appointment ID: {a.get('appointment_id')} | Patient ID: {a.get('patient_id')} | Date: {a.get('date')} | Time: {a.get('start_time')} | Status: {a.get('status')}")
            else:
                print(f"Appointment ID: {a.appointment_id} | Patient ID: {a.patient_id} | Date: {a.date} | Time: {a.start_time} | Status: {a.status}")
    if not found_any:
        print("You have no appointments.")


def doctor_view_patient_information(patient_list):
    print("---View Patient Information (Doctor)---")
    search_id = input("Enter the patient ID to look up (e.g., P-12345678): ").strip().upper()
    p = operations.find_record_by_id(patient_list, search_id)
    if not p:
        print("Error: Patient not found. Please check the ID.")
        return
    if isinstance(p, dict):
        print(f"ID: {p.get('user_id')} | Name: {p.get('name')} | Phone: {p.get('phone_number')}")
        print(f"Gender: {p.get('gender')} | DOB: {p.get('date_of_birth')} | Address: {p.get('address')}")
    else:
        print(f"ID: {p.user_id} | Name: {p.name} | Phone: {p.phone_number}")
        print(f"Gender: {p.gender} | DOB: {p.date_of_birth} | Address: {p.address}")


def doctor_update_appointment(doctor, appointment_list):
    print("---Update Appointment (Doctor)---")
    doctor_id = doctor.get('user_id') if isinstance(doctor, dict) else getattr(doctor, 'user_id', None)
    search_id = input("Enter the appointment ID to update: ").strip().upper()

    match = None
    for a in appointment_list:
        appt_id = a.get('appointment_id') if isinstance(a, dict) else getattr(a, 'appointment_id', None)
        appt_doctor_id = a.get('doctor_id') if isinstance(a, dict) else getattr(a, 'doctor_id', None)
        if appt_id == search_id and appt_doctor_id == doctor_id:
            match = a
            break

    if not match:
        print("Error: Appointment not found for this doctor. Please check the ID.")
        return

    new_status = input("Enter new status (Scheduled/Completed/Cancelled): ").strip()
    if isinstance(match, dict):
        match['status'] = new_status
    else:
        match.update_status(new_status)
    print(f"Appointment {search_id} updated to status: {new_status}")


def patient_book_appointment(patient, doctors, appointment_list):
    print("---Book an Appointment---")
    patient_id = patient.get('user_id') if isinstance(patient, dict) else getattr(patient, 'user_id', None)

    if not doctors:
        print("Sorry, there are no doctors registered yet.")
        return

    doctor_choice = input(
        "Would you like (a) any general doctor, or (b) to see a list of specialists to choose from? "
    ).strip().lower()

    if doctor_choice == "b":
        print("\nAvailable Doctors:")
        for d in doctors:
            if isinstance(d, dict):
                print(f"  {d.get('user_id')} - Dr. {d.get('name')} ({d.get('specialization')})")
            else:
                print(f"  {d.user_id} - Dr. {d.name} ({d.specialization})")
        doctor_id = input("Enter the Doctor ID you'd like to see: ").strip().upper()
        doctor = operations.find_record_by_id(doctors, doctor_id)
        if doctor is None:
            print("Error: Doctor not found. Please check the ID.")
            return
    elif doctor_choice == "a":
        doctor = doctors[0]
        doctor_id = doctor.get('user_id') if isinstance(doctor, dict) else getattr(doctor, 'user_id', None)
        doctor_name = doctor.get('name') if isinstance(doctor, dict) else getattr(doctor, 'name', None)
        print(f"You've been assigned to Dr. {doctor_name} ({doctor_id}).")
    else:
        print("Please choose 'a' or 'b'. Booking cancelled.")
        return

    target_date = input("Enter the date you'd like (YYYY-MM-DD): ").strip()
    available_slots = operations.get_available_time_slots(doctor, target_date, appointment_list)
    if not available_slots:
        print("Sorry, no available time slots for that doctor on that date.")
        return

    print("Available time slots:")
    for slot in available_slots:
        print(f"  {slot}")

    chosen_time = input("Enter the time slot you want (e.g. 09:00): ").strip()
    if chosen_time not in available_slots:
        print("That's not one of the available time slots. Booking cancelled.")
        return

    new_id = operations.generate_new_id_appointment()
    new_appointment = models.Appointment(new_id, patient_id, doctor_id, target_date, chosen_time, status="Scheduled")
    appointment_list.append(new_appointment)
    print(f"Appointment booked! Your appointment ID is {new_id}.")


def patient_cancel_appointment(patient, appointment_list):
    print("---Cancel My Appointment---")
    patient_id = patient.get('user_id') if isinstance(patient, dict) else getattr(patient, 'user_id', None)
    search_id = input("Enter the appointment ID to cancel: ").strip().upper()

    match = None
    for a in appointment_list:
        appt_id = a.get('appointment_id') if isinstance(a, dict) else getattr(a, 'appointment_id', None)
        appt_patient_id = a.get('patient_id') if isinstance(a, dict) else getattr(a, 'patient_id', None)
        if appt_id == search_id and appt_patient_id == patient_id:
            match = a
            break

    if match is None:
        print("Error: Appointment not found for you. Please check the ID.")
        return

    confirmation = input(f"Are you sure you want to cancel Appointment {search_id}? (yes/no): ").strip().lower()
    if confirmation == "yes":
        appointment_list.remove(match)
        print(f"Appointment {search_id} has been cancelled successfully.")
    else:
        print("Cancellation attempt aborted.")
 




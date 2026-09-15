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
            print(f"Appointment ID: {a.get('appointment_id')} | Patient ID: {a.get('patient_id')} | Doctor ID: {a.get('doctor_id')} | Date: {a.get('appointment_date')}")
        else:
            print(f"Appointment ID: {a.appointment_id} | Patient ID: {a.patient_id} | Doctor ID: {a.doctor_id} | Date: {a.appointment_date}")

def admin_cancel_appointment(appointment_list):
    print("---Cancel Appointment (Admin)---")
    search_id = input("Enter the appointment ID to cancel: ").strip().upper()
    found = False

    for a in appointment_list:
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
        appointment_list.remove(a)
        print(f"Appointment {search_id} has been cancelled successfully.")
    else:
        print("Attempt Cancelled.")

def patient_view_information():
    print("---View Patient Information---")
     
def patient_book_appointment():
    pass
def patient_view_appointment():
    pass
def patient_cancel_appointment():
    pass


 




from data_manager import load_data, save_data
from operations import find_record_by_id, check_pin
import sub_main

print("========================================")
print("Clinic Appointment And Management System")
print("========================================")



def admin_menu(patients, doctors, appointments):
    while True:
        print("=====ADMINISTRATOR MENU=====")
        print("1.Register new patient")
        print("2.Display all patients")
        print("3.Search patient")
        print("4.Update patient information")
        print("5.Add doctor")
        print("6.View appointments")
        print("7.Logout")

        try:
            choice = int(input("Choose an option (1-7): "))
        except ValueError:
            print("Please enter a number between 1 and 7.")
            continue

        if choice < 1 or choice > 7:
            print("Please choose a number between 1 and 7.")
            continue

        if choice == 1:
            sub_main.admin_register_patient(patients)
        elif choice == 2:
            sub_main.admin_display_patients(patients)
        elif choice == 3:
            sub_main.admin_search_patient(patients)
        elif choice == 4:
            sub_main.admin_update_patient(patients)
        elif choice == 5:
            sub_main.admin_add_doctor(doctors)
        elif choice == 6:
            sub_main.admin_view_appointments(appointments)
        elif choice == 7:
            print("Logging out...")
            break


def doctor_menu(record, patients, appointments):
    while True:
        print("=====DOCTOR MENU=====")
        print("1.View appointment")
        print("2.View patient information")
        print("3.Update appointment")
        print("4.Logout")

        try:
            choice = int(input("Choose an option (1-4): "))
        except ValueError:
            print("Please enter a number between 1 and 4.")
            continue

        if choice < 1 or choice > 4:
            print("Please choose a number between 1 and 4.")
            continue

        if choice == 1:
            sub_main.doctor_view_appointments(record, appointments)
        elif choice == 2:
            sub_main.doctor_view_patient_information(patients)
        elif choice == 3:
            sub_main.doctor_update_appointment(record, appointments)
        elif choice == 4:
            print("Logging out...")
            break


def patient_menu(record, doctors, appointments):
    while True:
        print("========PATIENT MENU========")
        print("1.View my infomation")
        print("2.Book appointment")
        print("3.View my appointment")
        print("4.Cancel appointment")
        print("5.Logout")

        try:
            choice = int(input("Choose an option (1-5): "))
        except ValueError:
            print("Please enter a number between 1 and 5.")
            continue

        if choice < 1 or choice > 5:
            print("Please choose a number between 1 and 5.")
            continue

        if choice == 1:
            sub_main.patient_view_information(record)
        elif choice == 2:
            sub_main.patient_book_appointment(record, doctors, appointments)
        elif choice == 3:
            sub_main.patient_view_own_appointments(record, appointments)
        elif choice == 4:
            sub_main.patient_cancel_appointment(record, appointments)
        elif choice == 5:
            print("Logging out...")
            break

def main():  # this particular function will control the main flow
    patients, doctors, appointments, admins = load_data()

    try:
        while True:
            #Keep the system running until the user chooses to exit
            print("Clinic system is running ...")

        #Ask the user for their ID or type Exit
            user_id =input("Enter your ID ,type NEW for registration,or Exit to close: ")

            if user_id.lower() =="exit":
                #close the system when the user chooses Exit
                print("Thank you for using the Clinic Management System.")
                print("System closed successfully")
                break

            elif user_id.upper() =="NEW":  #start the registration process for a new patient
                print("Starting new patient registration")
                sub_main.patient_self_registration_menu(patients)

            elif user_id.startswith("A-"): # An ID starting with A belongs to the Adminstrator
                record = find_record_by_id(admins, user_id)
                if record is None:
                    print("Invalid ID.Please enter a valid ID.")
                else:
                    entered_pin = input("Enter your PIN: ")
                    if check_pin(record, entered_pin):
                        print("Opening Admin Menu... ")
                        admin_menu(patients, doctors, appointments)
                    else:
                        print("Incorrect PIN.")

            elif user_id.startswith("DR-"):
                record = find_record_by_id(doctors, user_id)
                if record is None:
                    print("Invalid ID.Please enter a valid ID.")
                else:
                    entered_pin = input("Enter your PIN: ")
                    if check_pin(record, entered_pin):
                        print("Opening Doctor Menu... ")
                        doctor_menu(record, patients, appointments)
                    else:
                        print("Incorrect PIN.")

            elif user_id.startswith("P-"):
                #an ID starting with P belongs to a patient.
                record = find_record_by_id(patients, user_id)
                if record is None:
                    print("Invalid ID.Please enter a valid ID.")
                else:
                    entered_pin = input("Enter your PIN: ")
                    if check_pin(record, entered_pin):
                        print("Opening Patient Menu")
                        patient_menu(record, doctors, appointments)
                    else:
                        print("Incorrect PIN.")

            else:
                #this runs when the ID does not match
                #any of the accepted ID formats
                print("Invalid ID.Please enter a valid ID.")

    except KeyboardInterrupt:
        print("\nInterrupted - saving your data before closing.")
    finally:
        save_data(patients, doctors, appointments, admins)

    print("Welcome to the System!")

main()
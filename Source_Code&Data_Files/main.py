import validation
import sub_main
import models
from data_manager import load_data,save_data
from operations import find_record_by_id



def main():# this particular function will control the main flow
            # of the application'

# load saved data while the program starts
    patients, doctors, appointments, admins = load_data()

    try:
        while True:
            # display the opening screen

            print("\n=============================================")
            print("Clinic Appointment And Management System")
            print("=============================================\n")
            print("Welcome!")

            user_id = input("\nEnter your ID, type NEW to register as a patient, or Exit to close: ").strip().upper()

            #Option: Safe Shutdown
            if user_id == "EXIT":
                print("\nThank you using our Clinic Management System.")
                print("System closed successfully!")
                break

            #Option: Public Account Creation
            elif user_id == "NEW":
                print("\n=============================")
                print(" Patient Self-Registration")
                print("=============================\n")
                #Opens the patient registration interface
                sub_main.patient_self_registration_menu(patients)

            # ---ADMINISTRATOR LOGIN ---
            elif user_id.startswith("A-"):
                record = find_record_by_id(admins, user_id)

                if record:
                    entered_pin = input("Enter your 4-digit PIN: ").strip()
                    #Securely extract PIN regardless of if object is dict or class instance
                    record_pin = str(record.get('pin')) if isinstance(record, dict) else str(record.pin)
                    if entered_pin == record_pin:
                        #Build the real Admin object for this session so the rest of the
                        #program is working with the actual class, not just a dict
                        if isinstance(record, dict):
                            current_admin = models.Admin(record['user_id'], record['name'], record['pin'], record['phone_number'])
                        else:
                            current_admin = record
                        print("Login successful")
                        print("\nOpening Administrator Menu...")
                        admin_menu(current_admin, patients, doctors, appointments, admins)
                    else:
                        print("Incorrect PIN")
                else:
                    print("Administrator ID not found.")

            # --Doctor Login--  
            elif user_id.startswith("DR-"):

                record = find_record_by_id(doctors, user_id)

                if record:
                    entered_pin=input("Enter your 4 digit PIN: ").strip()
                    #Securely extract PIN regardless of if object is dict or class instance
                    record_pin = str(record.get('pin')) if isinstance(record,dict) else str(record.pin)
                    if entered_pin == record_pin:
                        #Build the real Doctor object for this session
                        if isinstance(record, dict):
                            current_doctor = models.Doctor(
                                record['user_id'], record['name'], record['pin'], record['phone_number'],
                                record.get('specialization'), record.get('shift_start_time'), record.get('shift_end_time')
                            )
                        else:
                            current_doctor = record
                        print("Login successful")
                        print("\nOpening Doctor Menu...")
                        doctor_menu(current_doctor, doctors, patients, appointments)
                    else:
                        print("Incorrect PIN")
                else:
                    print("Doctor ID not found.")

            elif user_id.startswith("P-"):

                # ---PATIENT LOGIN---
                record = find_record_by_id(patients, user_id)

                if record:
                    entered_pin = input("Enter your 4-digit PIN: ").strip()
                    # Securely extract PIN regardless of if object is dict or class instance
                    if isinstance(record, dict):
                        record_pin = str(record.get("pin"))
                    else:
                        record_pin = str(record.pin)

                    if entered_pin == record_pin:
                        #Build the real Patient object for this session
                        if isinstance(record, dict):
                            current_patient = models.Patient(
                                record['user_id'], record['name'], record['pin'], record['phone_number'],
                                record.get('gender'), record.get('date_of_birth'), record.get('email'), record.get('address')
                            )
                        else:
                            current_patient = record
                        print("Login successful")
                        print("\nOpening Patient Menu...")
                        patient_menu(current_patient, patients, doctors, appointments)
                    else:
                        print("Incorrect PIN.")
                else:
                    print("Patient ID not found.")
            else:
                print("Invalid ID format. Please try again.")
    except KeyboardInterrupt:
        print("\n\nInterrupted - saving your data before closing.")
    finally:
        #Runs on every exit path (normal exit, Ctrl+C, or a crash) so data is
        #never lost because the loop ended before reaching the EXIT branch.
        print("\nSaving system data...")
        save_data(patients, doctors, appointments, admins)


    #This ensures main() is only run if this script is executed directly
    
#This starts the program by calling the main function
        
            


def admin_menu(current_admin, patients, doctors, appointments, admins):
    #This function displays the options available
    #to an administrator.

    while True:
        print("\n=========================")
        print("   Administrator Menu   ")
        print("=========================\n")
        print("1.Register new patient")
        print("2.Display all  patients")
        print("3.Search patient")
        print("4.Update patient information")
        print("5.Delete patient profile")
        print("6.Add new doctor")
        print("7.Display all doctors")
        print("8.Search doctor")
        print("9.Update doctor profile")
        print("10.Delete doctor profile")
        print("11.View all appointments")
        print("12.Cancel appointment")
        print("13.Logout")


        choice = validation.get_valid_admin_menu()

        

        if  choice ==13:
            print("\nLogging out from Admin session...")
            break

        elif choice ==1:
            sub_main.admin_register_patient(patients)

        
        elif choice == 2:
            sub_main.admin_display_patients(patients)

        elif choice ==3:
            sub_main.admin_search_patient(patients)

        elif choice ==4:
            sub_main.admin_update_patient(patients)

        elif choice ==5:
            sub_main.admin_delete_patient(patients)

        elif choice ==6:
            sub_main.admin_add_doctor(doctors)

        elif choice ==7:
            sub_main.admin_display_doctors(doctors)
                        
        elif choice ==8:
            sub_main.admin_search_doctor(doctors)
                        
        elif choice ==9:
            sub_main.admin_update_doctor(doctors)

        elif choice ==10:
            sub_main.admin_delete_doctor(doctors)

        elif choice ==11:
            sub_main.admin_view_appointments(appointments)
        
        elif choice ==12:
            sub_main.admin_cancel_appointment(appointments)

    
        
                                
        
    
                                
                                
    

def  doctor_menu(current_doctor, doctors, patients, appointments):
    """
    Displays the doctor menu and routes choices to the functions in sub_main.py.
    """

    #Get the doctor's name whether the record is a dictionary
    #or Doctor object.
    if isinstance(current_doctor,dict):
        doc_name = current_doctor.get("name")
    else:
        doc_name = current_doctor.name

    while True:
        print("\n===================================")
        print(f"  Doctor Menu - Dr. {doc_name} ")
        print("===================================\n")
        print("1.View My Schedule")
        print("2.View My profile")
        print("3.Update Appointment Status")
        print("4.Logout")
        # get a valid doctor menu choice.
        choice = validation.get_valid_doctor_menu()

        if choice == 4:
            print("\nLogging out...")
            break

        elif choice == 1:
            sub_main.doctor_view_schedule(current_doctor,appointments,patients)
            print("View appointment")

        elif choice == 2:
            sub_main.doctor_view_profile(current_doctor)
            print("View patient information")

        elif choice == 3:
            sub_main.doctor_update_appointment_status(current_doctor,appointments)

        else:
            print("Invalid option.Please choose a number from 1 to 4")


        


def patient_menu(current_patient, patients, doctors, appointments):
    """
    Displays the Patient menu and routes choices to the functions in sub_main.py
    """
    if isinstance(current_patient, dict):
        patient_name = current_patient.get("name")
    else:
        patient_name = current_patient.name

    #Get the patient's name whether the record is a dictionary or a Patient object
    if isinstance(current_patient, dict):
        patient_name = current_patient.get("name")
    else:
        patient_name = current_patient.name

    while True:
        print("\n=======================================")
        print(f"    Patient Menu - {patient_name}")
        print("=======================================\n")
        print("1. View my information")
        print("2. Book appointment")
        print("3. View my appointment")
        print("4. Cancel appointment")
        print("5. Logout")


        choice = validation.get_valid_patient_menu()

    

        if choice ==5:
            print("\nLogging out...")
            break 

        elif choice == 1:
            sub_main.patient_view_information(current_patient)


        elif choice == 2:
            sub_main.patient_book_appointment(current_patient, doctors, appointments)
        
        elif choice == 3:
            sub_main.patient_view_appointments(current_patient,appointments)

        elif choice == 4:
            sub_main.patient_cancel_appointment(current_patient,appointments)
            

        

#start the application
if __name__ == "__main__":
    main()

import validation
import sub_main
from data_manager import load_data,save_data
from operations import find_record_by_id



def main():# this particular function will control the main flow
              #of the application'

#load saved data while the program starts
    patients, doctors, appointments, admins = load_data()

    while True:
        #display the opening screen

        print("\n=============================================")
        print("Clinic Appointment And Management System")
        print("=============================================\n")
        print("Welcome!")

        print("\n1. Login")
        print("2. Create Account(Patients Only) ")
        print("3. Exit")
        

        choice = validation.get_valid_menu()

        #option 1 :login routing      
        if choice == 1:
               #Ask the user for their ID 
            user_id = input("Enter your ID: ").strip().upper()

            # ---ADMINISTRATOR LOGIN ---
          
            if user_id.startswith("A-"):
                print("Administrator Login is not connected yet.")
# An ID starting with A belongs to the Administrator
# Hardcoded emergency backdoor so the system can be accessed
# if admins.json is missing or not configured yet.
                print("Administrator login is not connected yet.")
                if user_id =="A-ADMIN":
                    entered_pin = input("Enter your 4-digit PIN: ").strip()
                    if entered_pin =="1234":
                       print("\nOpening Administrator Menu...")
                       admin_menu(user_id, patients, doctors, appointments, admins)

                else:
                     print("Incorrect Password")   

                     #--Doctor Login  
            elif user_id.startswith("DR-"):
               
                user = find_record_by_id(doctors, user_id)

                if user:
                    entered_pin=input("Enter your 4 digit PIN: ").strip()
                    #Securely extract PIN regardless of if object is dict or class instance
                    user_pin = str(user.get('pin')) if isinstance(user,dict) else str(user.pin)
                    if entered_pin == user_pin:
                        print("\nOpening Doctor Menu...")
                        doctor_menu(user_id,doctors,patients,appointments)
                    else:
                        print("Incorrect PIN")
                else:
                    print("Doctor ID not found.")

            elif user_id.startswith("P-"):

                
                # ---PATIENT LOGIN---
                user = find_record_by_id(patients, user_id)

                if user:
                    entered_pin = input("Enter your 4-digit PIN: ").strip()
                    # Securely extract PIN regardless of if object is dict or class instance
                    if isinstance(user, dict):
                        user_pin = str(user.get("pin"))
                    else:
                        user_pin = str(user.pin)

                    if entered_pin == user_pin:
                        print("\nOpening Patient Menu...")
                        patient_menu(user_id, patients, doctors, appointments)
                    else:
                        print("Incorrect PIN.")
                else:
                    print("Patient ID not found.")
            else:
                print("Invalid ID format. Please try again.")

        #Option 2:Public Account Creation
        elif choice == 2:
            print("\n=============================")
            print(" Patient Self-Registration")
            print("=============================\n")
            #Opens the patient registration interface
            sub_main.patient_self_registration_menu(patients)
                      

        #Option 3:Safe Shutdown
        elif choice ==3:
            print("\nSaving system data...")
            #Save the current data before closing
            save_data(patients, doctors, appointments, admins)
            print("Thank you using our Clinic Management System.")
            print("System closed successfully!")
            break
       


    #This ensures main() is only run if this script is executed directly
   
    
#This starts the program by calling the main function
        
            


def admin_menu(user_id, patients, doctors, appointments, admin):
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

     
        
                                
        
       
                                
                                
    

def  doctor_menu(user_id,doctors, patients, appointments):
    """
    Displays the doctor menu and routes choices to the functions in sub_main.py.
    """

    #Find the currently logged -in doctor
    current_doctor = find_record_by_id(doctors, user_id)


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
         #get a valid doctor menu choice.
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


        


def patient_menu(user_id, patients, doctors, appointments):
    """
    Displays the Patient menu and routes choices to the functions in sub_main.py
    """
    #Find the currently logged - in patient
    current_patient = find_record_by_id(patients, user_id)

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
            print("Logging out...")
            break 

        elif choice == 1:
           sub_main.patient_view_information(patients)


        elif choice == 2:
            sub_main.patient_book_information(patients, doctors, appointments)
        
        elif choice == 3:
            sub_main.patient_view_appointments(
                patients,appointments)

        elif choice == 4:
            sub_main.patient_cancel_appointment(patients,appointments)
            

        

#start the application
if __name__ == "__main__":
    main()



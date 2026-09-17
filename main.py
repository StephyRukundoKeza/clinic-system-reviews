from data_manager import load_data, save_data 

from validation import  get_valid_admin_menu
from validation import get_valid_doctor_menu
from validation import get_valid_patient_menu
from sub_main import patient_self_registration_menu


from operations import find_record_by_id


def main():# this particular function will control the main flow
              #of the application'

#load saved data while the program starts
    patients, doctors, appointments = load_data()

    while True:
        #display the opening screen

        print("========================================")
        print("Clinic Appointment And Management System")
        print("========================================")
        print()
        print("Welcome!")
        print()
        print("1.Login")
        print("2.Create Account ")
        print("3.Logout")
        print()

        #option 1 :login choice 
        choice = input("Choice an option: ").strip()
        if choice =="1":
               #Ask the user for their ID 
            user_id = input("Enter your ID: ").strip()

        #route the user based on their ID
            if user_id.startswith("A-"):
                     # An ID starting with A belongs to the Adminstrator
                print("Administrator login is not connected yet.")
                if user:
                       print("Opening Adminstrator Menu'...")
                       admin_menu(user_id)

                else:
                     print("Adminstrator ID not found")     
                                   
                
                    
        
            elif user_id.startswith("DR-"):
                    user = find_record_by_id(doctors, user_id)

                    if user:
                       print("Opening Doctor Menu... ")
                       #open the doctor's menu
                       doctor_menu(user_id)
                    else:
                         print("Doctor ID not found")
        
            elif user_id.startswith("P-"):
                    user = find_record_by_id(patients, user_id)

                    if user:
                        #An ID starting with P- belongs to patient
                       print("Opening Patient Menu ...")
                       patient_menu(user_id)
                       #an ID starting with P belongs to a patient.
                    else:
                         print("Patient ID not found.")
            else:
                        #this runs when the ID does not match
                        #any of the accepted ID formats
                        print("Invalid ID.Please enter a valid ID.")            


        #Option 2:Create Account
        elif choice=="2":
            print("Create Account")
            while True:
                 print()
                 print("==============")
                 print("Create Account")
                 print("==============")
                 print()
                 print("1.Create Admin Account")
                 print("2.Create Doctor Account")
                 print("3.Create Patient Account")
                 print("4.Back")


                 account_choice = input("Choose an option: ").strip()
                 if account_choice =="1":
                      print("Create Admin Account")

                 elif account_choice =="2":
                      print("Create Doctor Account")

                 elif account_choice =="3":
                      # opens the patient registration interface
                      register_patient(patients)

                 elif account_choice =="4":
                      print("Returning to main menu...")
                      break


                 else:
                      print("Invalid option. Please choose 1, 2, 3, or 4. ")


        #Option 3:closing the system
        elif choice =="3":
            print("Thank you for using our Clinic Management System.")
            print("System closed successfully!")
       


            #save the current data before closing
            save_data(patients, doctors, appointments)

            break

        
        else:
             print("Invalid option. Please choose 1, 2, 3.")



    
#This starts the program by calling the main function
        
            


def admin_menu(user_id):
    #This function displays the options available
    #to an adminstrator.

    while True:
        print("=================")
        print("Adminstrator Menu")
        print("=================")
        print("1.Register new patient")
        print("2.Display all  patients")
        print("3.Search patient")
        print("4.Update patient information")
        print("5.Add doctor")
        print("6.View appointments")
        print("7.Logout")


        choice = get_valid_admin_menu()

        choice = input("Choose an option: ").strip()


        if  choice =="7":
            print("Logging out...")
            break

        elif choice =="1":

            print("Pegister new patient")

            #opens menu registration interface
            register_patient()



        elif choice =="2":
            print("Display all patient") 

        elif choice =="3":
            print("Search patients")

        elif choice =="4":
            print("Update patient information")

        elif choice =="5":
            print("Add doctor")

        elif choice =="6":
            print("View appointments")

        else:
            print("Invalid option. Please choose a number from 1 to 7.")



def  doctor_menu(user_id):
    #this function displays the options available to a doctor 


    while True:
        print("===========")
        print("Doctor Menu")
        print("===========")
        print("1.View appointment")
        print("2.View patient information")
        print("3.Update appointment")
        print("4.Logout")

        choice = get_valid_doctor_menu()  

        if choice =="4":
            print("Logging out...")
            break

        elif choice =="1":
            print("View appointment")

        elif choice =="2":
                    print("View patient information")

        elif choice =="3":
            print("Update appointment")

        else:
            print("Invalid option.Please choose a number from 1 to 4")


        


def patient_menu(user_id):
#this displays available options to a patient

    while True:
        print("============")
        print("Patient Menu")
        print("============")
        print("1.View my infomation")
        print("2.Book appointment")
        print("3.View my appointment")
        print("4.Cancel appointment")
        print("5.Logout")


        choice =   get_valid_patient_menu()

        choice = input("Choose an option: ").strip()


        if choice =="5":
            print("Logging out...")
            break 

        elif choice =="1":
            print("View my information")

        elif choice =="2":
            print("Book appointment")

        elif choice =="3":
            print("View my appointment")

        elif choice =="4":
            print("Cancel appointment")


        else:
            print("Invalid option.Please choose a number from 1 to 5.")
        
def register_patient(patients):
    #this function will collect the information
    #needed to register a new patient

    print("=====================")
    print("Patient Registration ")
    print("=====================")


    name = input("Enter your name: ")
    pin = input("Create a pin: ")
    phone_number = input("Enter your phone number: ")
    gender = input("Enter your gender: ")
    date_of_birth = input("Enter your date of birth: ")
    email = input("Enter your email: ")
    address = input("Enter your address: ")

    print()
    print("Patient information collected successfully.")
#start the application
main()       
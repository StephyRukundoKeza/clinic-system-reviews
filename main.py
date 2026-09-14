from data_manager import load_data, save_data 

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
        print("Enter your ID to continue.")
        print("Type NEW to register as patient. ")
        print("Type EXIT to close the system")
        print()



    #Ask the user for their ID  
        user_id =input("Enter your ID: ").strip()


        if user_id.lower() =="exit":
            #close the system when the user chooses Exit
            print("Thank you for using the Clinic Management System")
            print("System closed successfully")

            #save the current data before closing
            save_data(patients, doctors, appointments)

            break

        elif user_id.lower() =="new": 
             #start the registration process for a new patient
            register_patient()

        elif user_id.startswith("A-"):
             # An ID starting with A belongs to the Adminstrator
            print("Opening Adminstrator Menu...")
            admin_menu() 
            

        elif user_id.startswith("DR-"):
            print("Opening Doctor Menu... ")
            #open the doctor's menu
            doctor_menu()

        elif user_id.startswith("P-"):
            #An ID starting with P- belongs to patient
            print("Opening Patient Menu ...")

            patient_menu()
            #an ID starting with P belongs to a patient.
            


        else:
            #this runs when the ID does not match
            #any of the accepted ID formats
            print("Invalid ID.Please enter a valid ID.")


    
#This starts the program by calling the main function
        
            


def admin_menu():
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

        choice = int(input("Choose an option: "))

        if  choice =="7":
            print("Logging out...")
            break
        elif choice =="1":
            print("Pegister new patient")

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
            print("Option selected:",choice)



def  doctor_menu():
    #this function displays the options available to a doctor 


    while True:
        print("===========")
        print("Doctor Menu")
        print("===========")
        print("1.View appointment")
        print("2.View patient information")
        print("3.Update appointment")
        print("4.Logout")

        choice = input("Choose an option: ")

        if choice =="4":
            print("View appointment")
            break

        elif choice =="1":
            print("View appointment")

        elif choice =="2":
                    print("View patient information")

        elif choice =="3":
            print("Update appointment")

        else:
            print("Invalid option.Please choose a number from 1 to 4")


        


def patient_menu():


    while True:
        print("============")
        print("Patient Menu")
        print("============")
        print("1.View my infomation")
        print("2.Book appointment")
        print("3.View my appointment")
        print("4.Cancel appointment")
        print("5.Logout")

        choice = input("Choose an option: ")

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
            print("Invalid optiom.Please choose a number from 1 to 5.")
        
def register_patient():
    #this function will collect the information
    #needed to register a new patient

    print("=====================")
    print("Patient Registration ")
    print("=====================")


    name = input("Enter your name: ")
    phone_number = input("Enter your phone number: ")
    gender = input("Enter your gender: ")
    date_of_birth = input("Enter your date of birth: ")
    email = input("Enter your email: ")
    address = input("Enter your address: ")

    print()
    print("Patient information collected successfully.")
main()       
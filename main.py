print("========================================")
print("Clinic Appointment And Management System")
print("========================================")



def admin_menu():
    #This function displays the options available
    #to an adminstrator.

    while True:
        print("ADMINISTRATOR MENU")
        print("1.Register new patient")
        print("2.Display all patients")
        print("3.Search patient")
        print("4.Update patient information")
        print("5.Add doctor")
        print("6.View appointments")
        print("7.Logout")

        choice = input("Choose an option: ")

        if  choice =="7":
            print("Logging out...")
            break


        else:
            print("Option selected:",choice)



def  doctor_menu():
    #this function displays the options available to a doctor 


    while True:
        print("=====DOCTOR MENU=====")
        print("1.View appointment")
        print("2.View patient information")
        print("3.Update appointment")
        print("4.Logout")


        choice = input("Choose an option: ")


        if choice =="4":
            print("Logging out...")


        else:
            print("Option selected:", choice)



def patient_menu():


    while True:
        print("========PATIENT MENU========")
        print("1.View my infomation")
        print("2.Book appointment")
        print("3.View my appointment")
        print("4.Cancel appointment")
        print("5.Logout")

        choice = input("Choose an option ")

        if choice =="5":
            print("Logging out...")
            break


        else:
            print("Option selected:", choice)

def main():  # this particular function will control the main flow
   

    while True:
        #Keep the system running until the user chooses to exit
        print("Clinic system is running ...")  

    #Ask the user for their ID or type Exit 
        user_id =input("Enter your ID ,type NEW for registration,or Exit to close: ")

        if user_id =="Exit":
            #close the system when the user chooses Exit
            print("Thank you for using the Clinic Management System.")
            print("System closed successfully")
            break
        elif user_id =="NEW":  #start the registration process for a new patient
            print("Starting new patient registration")

        elif user_id.startswith("A-"): # An ID starting with A belongs to the Adminstrator

            admin_menu() 

            print("Opening Adminstrator Menu")

        elif user_id.startswith("DR-"):
            print("Opening Doctor Menu... ")
            #open the doctor's menu
            doctor_menu()

        elif user_id.startswith("P"):
            #an ID starting with P belongs to a doctor.
            print("Opening Patient Menu")


        else:
            #this runs when the ID does not match
            #any of the accepted ID formats
            print("Invalid ID.Please enter a valid ID.")


    print("Welcome to the System!")

main()
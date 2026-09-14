print("Day one on clinic appointment system!")
from datetime import datetime
def get_valid_menu():
    while True:
        try:
            menu=int(input("select an option(1-4): "))
            if menu=="":
                print("Oops sorry menu can not be left empty")
                continue
            if menu < 1 or menu > 4:
                print("Selection out of range. Please select a number from 1-4 ")
                continue
            break
        except ValueError:
            print("Invalid format. Select a number from 1-4 ")       
            
def get_valid_admin_menu():
    #This function displays the options available
    #to an adminstrator.

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
            choice = int(input("Choose an option(1-7): "))
            if choice=="":
                print("Oops sorry menu can not be left empty")
                continue
            if choice < 1 or choice > 7:
                print("Selection out of range. Please select a number from 1-7 ")
                continue
            break
        except ValueError:
           print("Invalid format. Select a number from 1-7 ")       
                    
def get_valid_doctor_menu()  :                 
    while True:
        print("=====DOCTOR MENU=====")
        print("1.View appointment")
        print("2.View patient information")
        print("3.Update appointment")
        print("4.Logout")
        try:
            choice = int(input("Choose an option(1-4): "))
            if choice=="":
                print("Oops sorry menu can not be left empty")
                continue
            if choice < 1 or choice > 4:
                print("Selection out of range. Please select a number from 1-7 ")
                continue
            break
        except ValueError:
            print("Invalid format. Select a number from 1-4 ")  
            
            
def get_valid_patient_menu():
    while True:
        print("========PATIENT MENU========")
        print("1.View my infomation")
        print("2.Book appointment")
        print("3.View my appointment")
        print("4.Cancel appointment")
        print("5.Logout")
        try:
            choice = int(input("Choose an option(1-5): "))
            if choice=="":
                print("Oops sorry menu can not be left empty")        
                continue
            if choice < 1 or choice > 5:
                print("Selection out of range. Please select a number from 1-7 ")
                continue
            break
        except ValueError:
                print("Invalid format. Select a number from 1-5 ")  
        
            
def get_valid_firstname():
   while True:
    firstname=input("Please enter your first name: ").strip()
    if firstname=="":
        print("Oops sorry first name can not be left empty")
        continue
    if not firstname.isalpha():
        print("Invalid format. Please enter a valid name")
        continue
    if firstname.isalpha():
        return  firstname      
                
def get_valid_lastname():
    while True:
        lastname=input("Please enter your last name: ").strip()
        if lastname=="":
            print("Oops sorry lasst name can not be left empty")
            continue
        if not lastname.isalpha():
            print("Invalid format. Please enter a valid name")
            continue
        if lastname.isalpha():
            return  lastname      
           
def get_valid_birthdate():
    while True:
        try:
            date_input= input("Please enter your date of birth with this format date as, YYYY-MM-DD: ")  # ask users for appointment date
            date = datetime.strptime(date_input, "%Y-%m-%d").date() 
            if date_input=="":
                print("Oops sorry date of birth can not be left empty enter a valid date")
                continue 
            break
        except ValueError:
            print("Invalid format. Please try again with this format date as, YYYY-MM-DD: ")
    return date       
                        
                            
def get_valid_appointmentdate():
    while True:
        try:
            date_input= input("Please enter your appointment date this format date as, YYYY-MM-DD: ")  # ask users for appointment date
            date = datetime.strptime(date_input, "%Y-%m-%d").date() 
            if date_input=="":
                print("Oops sorry date can not be left empty enter a valid date")
                continue 
            break
        except ValueError:
            print("Invalid format. Please try again with this format date as, YYYY-MM-DD: ")
    return date

def get_valid_phone_number():
    while True:
        number=input("Enter your mobile phone number(without the country code): ").strip()  # this ensures users do not enter country codes with have + at the beginning because the program is built to reject all non digit inputs
        if number=="": # non empy string
            print("Sorry your mobile phone number can not be empty")
            continue
        if not number.isdigit() : # checks that all the input only contains numbers
            print("Phone number must contain only numbers")
            continue
        if len(number)!=8:  # since the typical mauritian mobile number is 8 digits it checks to ensure a valid length is entered
            print("Phone number must be 8 digits")
            continue
        if number[0] !="5" and number[0]!="7": # checks that numbers entered starts with 5 or 7 which is the standard for mauritian numbers to ensure the number is valid
            print("Enter a valid mauritian number")
            continue
        break
    return number

def get_valid_email():
    while True:
        valid_domains = ["gmail.com", "yahoo.com", "outlook.com"]  # valid email domains to allow
        email=input("Enter a valid email address: ").strip()
        parts=email.split("@") #splits the email into two parts
        if email=="":
            print("Email can not be empty. Please enter a valid email address: ")
            continue
        if "@" and "." not in email:
            print("Invalid email format. Enter a valid format following this patient@gmail.com: ")
            continue
        if len(parts)!=2:
            print("Invalid email format. Enter a valid format following this patient@gmail.com: ")
            continue
        if parts[0]==""and parts[1]=="":
            print("Invalid email format. Enter a valid format following this patient@gmail.com: ")
            continue
        if parts[1] not in valid_domains:
            print("Invalid email format. Enter a valid email domain: ")
            continue
        break
    return email
    
#
get_valid_phone_number()

#get_valid_menu()
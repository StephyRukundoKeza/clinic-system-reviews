print("Day one on clinic appointment system!")
from datetime import datetime

def get_valid_menu():
    while True:
        try:
            menu=int(input("select an option(1-3): "))
            if menu=="":
                print("Oops sorry menu can not be left empty")
                continue
            if menu < 1 or menu > 3:
                print("Selection out of range. Please select a number from 1-3 ")
                continue
            break
        except ValueError:
            print("Invalid format. Select a number from 1-3")       
            
def get_valid_admin_menu():
    #This function displays the options available
    #to an administrator.

    while True:
       
        try:
            choice = int(input("Choose an option(1-13): "))
            if choice=="":
                print("Oops sorry menu can not be left empty")
                continue
            if choice < 1 or choice > 13:
                print("Selection out of range. Please select a number from 1-13 ")
                continue
            break
        except ValueError:
           print("Invalid format. Select a number from 1-13 ")       
                    
def get_valid_doctor_menu()  :                 
    while True:
    
        try:
            choice = int(input("Choose an option(1-4): "))
            if choice=="":
                print("Oops sorry menu can not be left empty")
                continue
            if choice < 1 or choice > 4:
                print("Selection out of range. Please select a number from 1-4 ")
                continue
            break
        except ValueError:
            print("Invalid format. Select a number from 1-4 ")  
            
            
def get_valid_patient_menu():
    while True:
       
        try:
            choice = int(input("Choose an option(1-5): "))
            if choice=="":
                print("Oops sorry menu can not be left empty")        
                continue
            if choice < 1 or choice > 5:
                print("Selection out of range. Please select a number from 1-5 ")
                continue
            break
        except ValueError:
                print("Invalid format. Select a number from 1-5 ")  
        
            
def is_valid_name(name):
    return name != "" and name.isalpha()

def get_valid_firstname():
    while True:
        firstname = input("Please enter your first name: ").strip()
        if firstname == "":
            print("Oops sorry first name can not be left empty")
            continue
        if not is_valid_name(firstname):
            print("Invalid format. Please enter a valid name")
            continue
        return firstname

def get_valid_lastname():
    while True:
        lastname = input("Please enter your last name: ").strip()
        if lastname == "":
            print("Oops sorry last name can not be left empty")
            continue
        if not is_valid_name(lastname):
            print("Invalid format. Please enter a valid name")
            continue
        return lastname     
           
def get_valid_birthdate():
    while True:
        try:
            date_input= input("Please enter your date of birth with this format date as, YYYY-MM-DD: ")  # ask users for appointment date
            date = datetime.strptime(date_input, "%Y-%m-%d").date() 
            if date_input=="":
                print("Oops sorry date of birth can not be left empty enter a valid date")
                continue 
            if date>datetime.today().date(): # ensures the due date is not a date that has already past
                print("Birth date date cannot be after today's date.")
                continue
            break
        except ValueError:
            print("Invalid format. Please try again with this format date as, YYYY-MM-DD: ")
    return date       
                        
                            
def get_valid_appointment_date():
    while True:
        date_input = input(
            "Please enter your appointment date in this format (YYYY-MM-DD): "
        ).strip()
        if date_input == "":
            print("Oops, appointment date cannot be left empty.")
            continue

        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid format. Please try again with this format (YYYY-MM-DD): ")
            continue

        if date < datetime.today().date():
            print("Appointment date cannot be before today's date.")
            continue

        return date

def get_valid_phone_number():
    while True:
        number=input("Enter your mobile phone number(without the country code): ").strip()  # this ensures users do not enter country codes with have + at the beginning because the program is built to reject all non digit inputs
        if number=="": # non-empty string
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
def is_valid_duration(duration_minutes):
    return isinstance(duration_minutes, (int, float)) and duration_minutes > 0

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
    
#get_valid_birthdate()

#get_valid_menu()

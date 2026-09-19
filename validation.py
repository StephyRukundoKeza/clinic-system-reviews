print("Day one on clinic appointment system!")
from datetime import datetime

from operations import get_available_time_slots

def get_valid_menu():
    #This function displays the options available
        #to an administrator.
    while True:
        try:
            menu=int(input("select an option(1-3): "))
            if menu=="":  #check for my empty string inputs
                print("Oops sorry menu can not be left empty")
                continue
            if menu < 1 or menu > 3:
                print("Selection out of range. Please select a number from 1-3 ")
                continue
        
            return menu
        except ValueError:
            print("Invalid format. Select a number from 1-3")    
            
def get_valid_create_account_menu():
    while True:
        try:
            menu=int(input("select an option(1-4): "))
            if menu=="":  #check for my empty string inputs
                print("Oops sorry menu can not be left empty")
                continue
            if menu < 1 or menu > 4:
                print("Selection out of range. Please select a number from 1-3 ")
                continue
               
            return menu
        except ValueError:
                print("Invalid format. Select a number from 1-3")    
            
def get_valid_admin_menu():
    #This function displays the options available
    #to an administrator.

    while True:
       
        try:
            choice = int(input("Choose an option(1-7): "))
            if choice=="": #check for my empty string inputs
                print("Oops sorry menu can not be left empty")
                continue
            if choice < 1 or choice > 7:
                print("Selection out of range. Please select a number from 1-7 ")
                continue
            return choice
        except ValueError:
           print("Invalid format. Select a number from 1-7 ")       
                    
def get_valid_doctor_menu() :   
    #This function displays the options available
    #to a doctor.              
    while True:
    
        try:
            choice = int(input("Choose an option(1-4): "))
            if choice=="":
                print("Oops sorry menu can not be left empty")
                continue
            if choice < 1 or choice > 4:
                print("Selection out of range. Please select a number from 1-7 ")
                continue
            return choice
        except ValueError:
            print("Invalid format. Select a number from 1-4 ")  
            
            
def get_valid_patient_menu():
        #This function displays the options available
    #to a menu
    
    while True:
       
        try:
            choice = int(input("Choose an option(1-5): "))
            if choice=="":
                print("Oops sorry menu can not be left empty")        
                continue
            if choice < 1 or choice > 5:
                print("Selection out of range. Please select a number from 1-7 ")
                continue
            return choice
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
            print("Oops sorry last name can not be left empty")
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
            if date>datetime.today().date(): # ensures the due date is not a date that has already past
                print("Birth date date cannot be after today's date.")
                date_input=input("Enter another date(YYYY-MM-DD: ")
                continue
            break
        except ValueError:
            print("Invalid format. Please try again with this format date as, YYYY-MM-DD: ")
    return date       
                        
                            
def get_valid_appointment_date():
    while True:
        try:
            date_input= input("Please enter your appointment date this format date as, YYYY-MM-DD: ")  # ask users for appointment date
            date = datetime.strptime(date_input, "%Y-%m-%d").date() 
            if date_input=="":
                print("Oops sorry date can not be left empty enter a valid date")
                continue 
            if date<datetime.today().date(): # ensures the due date is not a date that has already past
                print("Appointment date cannot be before today's date.")
                date_input=input("Enter another date(YYYY-MM-DD: ")
                continue
            
                      
            return date
           
        except ValueError:
            print("Invalid format. Please try again with this format date as, YYYY-MM-DD: ")
    
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
     
        return email
    
def get_valid_doctor_choice(doctors):
    while True:
            try:
                choice=int(input('select a doctor number'))
    
    
                if choice <1 or choice >len(doctors):
                    print("sorry, selection out of range")
                    continue
                return choice
            except ValueError:
                print(f"Invalid format. Please enter a number between 1 and {len(doctors)}")
   
            
            


def get_valid_slot_choice(available_slots):
    while True:
        try:
            slot_choice= int(input('select a slot number'))
            if slot_choice <1 or slot_choice >len(available_slots):
                print("sorry, selection out of range")
                continue
            return slot_choice 
                
        except ValueError:
            print(f"Invalid format. Please enter a number between 1 and {len(available_slots)}")
           
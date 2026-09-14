#models.py
#This file will contain the parent User class, 
#the child classes (Admin, Doctor, Patient) 
#demonstrating inheritance, and the standalone Appointment class.
#Takes input and stores it in a dictionary format for easy retrieval and management of user and appointment data.


#This is the parent class for all users who log into the clinic appointment system
class User:

    def __init__(self, user_id, name, pin, phone_number):
        self.user_id = user_id
        self.name = name
        self.pin = pin
        self.phone_number = phone_number

    def verify_pin(self, input_pin):   #verifies the user's pin for authentication
        return self.pin == input_pin

    def to_dict(self):  #converts the user object to a dictionary for easy storage and retrieval
        return {
            "user_id": self.user_id,
            "name": self.name,
            "pin": self.pin,
            "phone_number": self.phone_number
        }


class Admin(User):  #Admin class inherits from User class
    def __init__(self, user_id, name, pin, phone_number):
            #call the parent class (User) constructor  
            super().__init__(user_id, name, pin, phone_number)  

    def to_dict(self):  #overrides the to_dict method to include the role of the user
        data = super().to_dict()
        data["role"] = "Admin"
        return data

class Doctor(User):   #Doctor class inherits from User class
    def __init__(self, user_id, name, pin, phone_number, specialization, shift_start_time, shift_end_time):
        super().__init__(user_id, name, pin, phone_number)
        self.specialization = specialization
        self.shift_start_time = shift_start_time
        self.shift_end_time = shift_end_time

    def update_shifts(self, shift_start_time, shift_end_time):  #method to update the doctor's shifts
        self.shift_start_time = shift_start_time
        self.shift_end_time = shift_end_time

    def to_dict(self):   #overrides the to_dict method to include the role of the user, specialization, and shifts
        data = super().to_dict()
        data["role"] = "Doctor"
        data["specialization"] = self.specialization
        data["shift_start_time"] = self.shift_start_time
        data["shift_end_time"] = self.shift_end_time    
        return data


class Patient(User):  #Patient class inherits from User class
    def __init__(self, user_id, name, pin, phone_number, gender, date_of_birth, email, address, notification=None):
        super().__init__(user_id, name, pin, phone_number)
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.email = email
        self.address = address
        self.notification = notification
    
    def update_profile(self, name=None, phone_number=None, gender=None, date_of_birth=None, email=None, address=None):  #method to update the patient's profile
        updates = {"name": name, "phone_number": phone_number, "gender": gender, "date_of_birth": date_of_birth, "email": email, "address": address}
        for field, value in updates.items():
            if value is not None and hasattr(self, field):
                setattr(self, field, value)
        return True

    def add_notification(self, message):  #method to add a notification for the patient
        if self.notification is None:
            self.notification = []
        self.notification.append(message)

    def clear_notification(self):  #method to clear the patient's read notifications
        if self.notification is not None:
            self.notification = []

    def to_dict(self):  #overrides the to_dict method to include the role of the user
        data = super().to_dict()
        data["role"] = "Patient"
        data["gender"] = self.gender
        data["date_of_birth"] = self.date_of_birth
        data["email"] = self.email
        data["address"] = self.address
        data["notification"] = self.notification
        return data 

class Appointment:  #Appointment class to manage appointments
  def __init__(self, appointment_id, patient_id, doctor_id, date, start_time, duration_minutes=60, status="Active"):
    self.appointment_id = appointment_id
    self.patient_id = patient_id
    self.doctor_id = doctor_id
    self.date = date
    self.start_time = start_time
    self.duration = duration_minutes  # Duration in minutes
    self.status = status    

    def update_status(self, new_status):  #method to update the status of the appointment (e.g., Active, Completed, Cancelled)
        self.status = new_status

    def reschedule_appointment(self, new_date, new_start_time):  #method to reschedule an existing appointment
        self.date = new_date
        self.start_time = new_start_time

    def to_dict(self):  #method to convert the appointment object to a dictionary for easy storage and retrieval
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date,
            "start_time": self.start_time,
            "duration": self.duration,
            "status": self.status
        }



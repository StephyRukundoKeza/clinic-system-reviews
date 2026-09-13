print("Day one on clinic appointment system!")
import random

def generate_new_id_admin():
    print("Generating your admin id")
    id=random.randrange(00000000,99999999)
    print(f"Your admin id is A-{id}")
    return f"A-{id}"

def generate_new_id_patient():
    print("Generating your patients id")
    id=random.randrange(00000000,99999999)
    print(f"Your patient id is P-{id}")
    return f"P-{id}"

def generate_new_id_doctor():
    print("Generating your doctors id")
    id=random.randrange(00000000,99999999)
    print(f"Your patient id is DR-{id}")
    return f"DR-{id}"


def check_doctor_availability():
    pass
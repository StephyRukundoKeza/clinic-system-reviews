# Clinic Appointment & Patient Management System

## Group 5 - Programming 1 Summative Project

## Project Overview

The Clinic Appointment System is a robust, terminal-based Python application that allows a medical clinic to seamlessly manage its daily operations. Built with a focus on Object-Oriented Programming (OOP) and data persistence, the system features three distinct, secure user portals:

1. **Administrator Portal:** Full CRUD (Create, Read, Update, Delete) access for managing patient and doctor profiles, as well as viewing and cancelling the clinic's master schedule.
2. **Doctor Portal:** Allows doctors to securely log in, view their assigned daily schedules, update their working shift hours, and mark appointments as completed, active, or cancelled.
3. **Patient Portal:** Allows patients to self-register securely, view their profile, book new appointments based on dynamic doctor availability (preventing double-booking), and manage their schedule.

## System Architecture

To avoid merge conflicts, ensure clean code, and meet all grading rubrics, the application is modularized into six distinct Python files and four JSON data files:

### Application Logic Files

* **`main.py` (The Launcher):** The entry point of the application. It acts purely as a boot sequence and traffic controller. It loads the data on startup, handles the initial login/registration menu, passes control to the sub-menus, and safely saves all data on exit.
* **`sub_main.py` (The Interface & Routing):** Contains the user journey logic. It holds the overarching while loops for the Administrator, Doctor, and Patient menus, handles self-registration, and routes numerical menu choices to their corresponding actions.
* **`models.py` (The OOP Blueprints):** Contains the Object-Oriented structures. It features a parent `User` class demonstrating inheritance for the `Admin`, `Doctor`, and `Patient` child classes. It also includes the standalone `Appointment` class. Every class contains a `to_dict()` method for easy JSON serialization.
* **`operations.py` (The Business Logic):** The Brain of the system. It handles complex, multi-object logic such as automatically generating secure, sequential IDs and dynamically calculating free time slots based on a doctor's shift constraints and existing bookings.
* **`validation.py` (The Security Shield):** Contains robust `try/except` loops protecting the system from fatal crashes. It traps users in loops until they provide valid inputs (e.g., verifying YYYY-MM-DD date formats, standardizing phone numbers, checking email formatting, and securely intercepting empty string inputs).
* **`data_manager.py` (The Storage Controller):** Handles all file I/O operations. It utilizes Python's built-in `json` module to read and write system states, using exception handling to gracefully prevent application crashes if a JSON file is missing.

### Data Storage Files

The system utilizes local JSON files to maintain a persistent state between sessions.

* `admins.json`
* `doctors.json`
* `patients.json`
* `appointments.json`

## Team Members & Roles

This project was built collaboratively by dividing the system architecture into manageable domains:

* **Anita Otoo: System Integrator & Interface Lead** - Responsible for `main.py` and `sub_main.py`. Managed the overarching user experience, login loops, and menu routing.
* **Samuel Anagbah: OOP & Data Architect** - Responsible for `models.py`. Designed the object-oriented structure, implementing inheritance and object-to-dictionary serialization.
* **Stephy Rukundo: File Handling Specialist** - Responsible for `data_manager.py`. Managed persistent JSON data storage, ensuring data is not lost between sessions.
* **Chukwudumedi Ukogu: Quality Assurance & Logic Master** - Responsible for `operations.py` and `validation.py`. Wrote the complex business logic, dynamic time slot calculations, and bulletproof input validation.

## How to Run the Application

### Prerequisites

* Python 3.x installed on your local machine.
* Standard Python libraries used (`json`, `datetime`, `random`). No external packages are required.

### Execution

1. Clone or download this repository to your local machine.
2. Ensure all six `.py` files and the four `.json` files are in the same root directory.
3. Open your terminal or command prompt.
4. Navigate into the project directory.
5. Run the following command:

   ```bash
   python main.py
   ```

6. Follow the on-screen prompts at the opening menu:
   * Select **1** to log in with an existing ID (e.g., `A-100`, `DR-201`, `P-101`).
   * Select **2** to self-register as a new patient.
   * Select **3** to safely shut down the system and save all data to the JSON files.

### Emergency Admin Access

If you are starting the application with a completely empty `admins.json` file, you can access the Administrator menu to begin populating the system by selecting option 1 (Login), typing `A-ADMIN` as the User ID, and `1234` as the PIN.

## Testing and Error Handling

The system includes rigorous error handling to prevent runtime crashes:

* **Empty Input Checks:** The system catches accidental "Enter" keystrokes before they trigger `ValueError` crashes.
* **Date & Time Formatting:** Dates must be in `YYYY-MM-DD` format. Times must be in 24-hour `HH:MM` format. The system actively checks that birth dates and appointment dates are logically valid against the current calendar.
* **Double-Booking Prevention:** The application actively calculates a doctor's free time slots by cross-referencing their shift hours against the active `appointments.json` database.
* **File Safety:** If any `.json` database file is missing, the system will safely generate a new, empty list rather than throwing a `FileNotFoundError`.
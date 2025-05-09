import tkinter as tk

from patient import Patient
from visit import Visit
from note import Note
from user import User

from tkinter import messagebox, simpledialog, ttk
from loadingFiles import load_user, load_patients, load_notes
from add_patient import add_patient_data
from removing_patient import remove_patient_data
from retrieving_patient import retrieve_patient_data
from countvisits import counting_patient_visits
from view_notes import view_note
from stats import generate_management_statistics
from logging_activity import log_usage
import datetime
import csv

class HospitalUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Clinical System")
        self.username = load_user('Credentials.csv')
        self.patients_data = load_patients('Patient_data.csv')
        self.notes_data = load_notes('Notes.csv', 'Patient_data.csv', self.patients_data)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.build_login_ui()

    
    def build_login_ui(self):
        tk.Label(self.root, text = "Username").pack()
        tk.Entry(self.root, textvariable = self.username_var).pack()

        tk.Label(self.root, text = "Password").pack()
        tk.Entry(self.root, textvariable = self.password_var, show = '*').pack()

        tk.Button(self.root, text = "Login", command = self.authenticate_user).pack()
        
    def authenticate_user(self):
        username = self.username_var.get()
        password = self.password_var.get()
        user = User(username, password)
        
        if user.authenticate(username, password):
            self.user = user # store user object 
            self.root.withdraw()
            self.main_menu(user)
            
            log_usage(username, user.role, "Login", "Success")
        else:
            messagebox.showerror("Login Failed. ", "Invalid username or password.")
            log_usage(username, "Unknown", "Login", "Failed")

    def main_menu(self, user):
        role = user.role.lower()

        menu = tk.Toplevel()
        menu.title(role.capitalize() + " menu")

        tk.Label(menu, text = ("Welcome " + user.username + ", " +  role)).pack(pady = 10)

        if role in ['nurse', 'clinician']:
            tk.Button(menu, text = "Add Patient", command = self.add_patient_ui).pack()
            tk.Button(menu, text = "Remove Patient", command=self.remove_patient_ui).pack()
            tk.Button(menu, text = "Retrieve Patient", command=self.retrieve_patient_ui).pack()
            tk.Button(menu, text = "Count Visits", command=lambda: counting_patient_visits(self.patients_data)).pack()
            tk.Button(menu, text = "View Notes by Date", command=self.view_note_ui).pack()
            tk.Button(menu, text = "Logout", command = lambda: [menu.destroy(), self.root.deiconify()]).pack(pady = 10)

        elif role == 'admin':
            tk.Button(menu, text = "Count Visits", command=lambda: counting_patient_visits(self.patients_data, self.user)).pack()
            tk.Button(menu, text = "Logout", command = lambda: [menu.destroy(), self.root.deiconify()]).pack(pady = 10)

        elif role == 'management':
            tk.Button(menu, text = "Generate Statistics", command = lambda: self.show_message(generate_management_statistics(self.patients_data))).pack()
            tk.Button(menu, text = "Logout", command = lambda: [menu.destroy(), self.root.deiconify()]).pack(pady = 10)

    
    def show_message(self, text):
        messagebox.showinfo("Result:/n", str(text))


    
# create window for adding patient
    def add_patient_ui(self):
        new_window = tk.Toplevel()
        new_window.title("Check for Patient")

        tk.Label(new_window, text = "Enter Patient ID").pack()
        patientID_entry = tk.Entry(new_window)
        patientID_entry.pack()
        

        def patient_checker():
            patient_id = patientID_entry.get()
                
            if patient_id in self.patients_data:
                messagebox.showinfo("Patient Found", "Adding visit for existing patient")
                existing_patient = self.patients_data[patient_id]

                ask_info(patient_id, existing_patient)     
            else: 
                messagebox.showinfo("New Patient", "Creating new patient record")
                ask_info(patient_id, None)

            new_window.destroy()
            
        tk.Button(new_window, text="Check Patient", command = patient_checker).pack()

        def ask_info(patient_id, existing_patient):
            form_window = tk.Toplevel()
            form_window.title("Add Visitation Details:")

            if existing_patient:
                info_prompts = [ 'Visit_time', 'Visit_department', 'Chief_complaint', 'Note_ID', 'Note_type', 'Note_text']
                
            else: 
                info_prompts = ['Gender', 'Race',  'Age',  'Ethnicity',  'Zip_code',  'Insurance',  'Visit_time',  'Visit_department',  'Chief_complaint',  'Note_ID',  'Note_type',  'Note_text']
            
            inputs = {}
            for prompt in info_prompts:
                tk.Label(form_window, text = prompt).pack()
                info_entry = tk.Entry(form_window)
                info_entry.pack()
                inputs[prompt] = info_entry

            def check_non_empty_inputs():
                for entry in inputs.values():
                    if not entry.get().strip(): 
                        return False 
                return True 
                
            def date_checker(date):        
                try: # Check basic format YYYY-MM-DD
                    if len(date) == 10 and date[4] == '-' and date[7] == '-':
                        return True
                    else:
                        print("Invalid date format. Please enter the date as YYYY-MM-DD.\n")
                except ValueError:
                    return False

                    
            def submit():
                if not check_non_empty_inputs():
                    messagebox.showerror("Error", "All fields must be filled.")
                    log_usage(self.user.username, self.user.get_role(), "ADD Patient", "Failed")
                    return

                visit_date = inputs['Visit_time'].get().strip()
                if not date_checker(visit_date):
                    messagebox.showerror("Invalid date", "Visit Time must be in YYYY-MM-DD")                    
                    log_usage(self.user.username, self.user.get_role(), "ADD Patient", "Failed")

                    return
                try:
                    data = {}                    
                    for entries in info_prompts:
                        value = inputs[entries].get()
                        data[entries] = value
                    add_patient_data(self.patients_data, patient_id, data)
                    messagebox.showinfo("Success!","Patient added.")
                    form_window.destroy()
                    log_usage(self.user.username, self.user.role, "ADD Patient", "Success")

                except Exception as e: 
                    messagebox.showerror("Error", str(e))

            tk.Button(form_window, text = "Submit", command = submit).pack()
        

# create window for removing patient
    def remove_patient_ui(self):
        new_window = tk.Toplevel()
        new_window.title("Remove Patient")
        
        tk.Label(new_window, text = "Enter Patient ID:").pack()
        patientID_entry = tk.Entry(new_window)
        patientID_entry.pack()
        
        tk.Button(new_window, text = "Remove", command = lambda: self.call_remove_patient(patientID_entry.get(), new_window)).pack()

    def call_remove_patient(self, patientID, new_window):
        if remove_patient_data(self.patients_data, patientID, 'Patient_data.csv', 'Notes.csv'):
            messagebox.showinfo("Removed", "Patient ID " + patientID + " data has been successfully removed from the file.")
            log_usage(self.user.username, self.user.role, "REMOVE Patient", "Success")

            new_window.destroy()
        else:
            messagebox.showinfo("Error", "Patient "+ patientID + " could not be removed.")
            log_usage(self.user.username, self.user.role, "REMOVE Patient", "Failed")


# create window for retrieving patient
    def retrieve_patient_ui(self):
        new_window = tk.Toplevel()
        new_window.title("Retrieve Patient")
        
        tk.Label(new_window, text = "Enter Patient ID:").pack()
        patientID_entry = tk.Entry(new_window)
        patientID_entry.pack()
        
        tk.Button(new_window, text = "Retrieve", command = lambda: self.call_retrieve(patientID_entry.get(), new_window)).pack()

    def call_retrieve(self, patientID,new_window):
        patient = self.patients_data.get(patientID)
    
        if patient:
            details_window = tk.Toplevel()
            details_window.title("Patient " + patientID + " Details!")
            if patient.records: 
                info = patient.records[0]
                info_frame = tk.Frame(details_window)
                info_frame.pack(pady = 15)
                
                tk.Label(info_frame, text = ("PATIENT ID: "+ patientID)).pack()
                tk.Label(info_frame, text = ("Gender: "+ info.gender)).pack()
                tk.Label(info_frame, text = ("Race: " + info.race)).pack()
                tk.Label(info_frame, text = ("Ethnicity: " + info.ethnicity)).pack()
                tk.Label(info_frame, text = ("Age: " + str(info.age))).pack()
                tk.Label(info_frame, text = ("Zip Code: "+ info.zip_code)).pack()
                tk.Label(info_frame, text = ("Insurance: " + info.insurance)).pack()
                log_usage(self.user.username, self.user.role, "RETRIEVE Patient", "Success")
            else:
                tk.Label(details_window, text = ("No visits recorded for this patient.")).pack()
        else: 
            messagebox.showinfo("Error", "Patient " + patientID + " not found.")
            log_usage(self.user.username, self.user.role, "RETRIEVE Patient", "Failed")
            
# create window for viewing patient notes
    def view_note_ui(self):
        new_window = tk.Toplevel()
        new_window.title("View Notes")

        tk.Label(new_window, text = "Enter Patient ID:").pack()
        patientID_entry = tk.Entry(new_window)
        patientID_entry.pack()
        
        tk.Label(new_window, text = "Enter Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(new_window)
        date_entry.pack()

        def show_notes():
            patient_id = patientID_entry.get()
            date = date_entry.get()
            notes = view_note(self.patients_data, patient_id, date)

            notes_display =  tk.Toplevel()
            notes_display.title("Notes for " + patient_id + " on " + date)

            if notes:
                for note_text in notes:
                    tk.Label(notes_display, text=note_text, justify = "left", anchor = "w", wraplength = 50).pack(padx = 10, pady = 5)
                    log_usage(self.user.username, self.user.role, "VIEW Notes", "Success")
            else:
                tk.Label(notes_display, text = "No notes found.").pack(pady = 10)
                log_usage(self.user.username, self.user.role, "VIEW Notes", "Failed")
            new_window.destroy()
            
        tk.Button(new_window, text = "View Notes", command = show_notes).pack()

        
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalUI(root)
    root.mainloop()

import tkinter as tk

from patient import Patient
from visit import Visit, Note
from user import User

from tkinter import messagebox, simpledialog, ttk
from loadingFiles import load_user, load_patients, load_notes
from add_patient import add_patient_data
from remove import remove_patient_data
from retrieve import retrieve_patient_data
from countvisits import counting_patient_visits
from view_notes import view_note
from stats import generate_management_statistics
import datetime
import csv

class HospitalUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Clinical System")
        self.username = load_user('./PA3_credentials.csv')
        self.patients_data = load_patients('./PA3_data.csv')
        self.notes_data = load_notes('PA3_notes.csv', 'PA3_data.csv', self.patients_data)

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
            self.root.withdraw()
            self.main_menu(user)
        else:
            messagebox.showerror("Login Failed. ", "Invalid username or password.")

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

        elif role == 'admin':
            tk.Button(menu, text = "Count Visits", command=lambda: counting_patient_visits(self.patients_data)).pack()

        elif role == 'management':
            tk.Button(menu, text = "Generate Statistics", command = lambda: self.show_message(generate_management_statistics(self.patients_data))).pack()
            tk.Button(menu, text = "Logout", command = lambda: [menu.destroy(), self.root.deiconify()]).pack(pady = 10)

    
    def show_message(self, text):
        messagebox.showinfo("Result:/n", str(text))


    
# create window for adding patient
    def add_patient_ui(self):
        new_window = tk.Toplevel()
        new_window.title("Add Patient")

        entries = ["Patient ID", "Gender", "Race", "Ethnicity", "Age", "Zip Code", "Insurance", "Complaint"]

        self.patient_entries ={}

        for entry in entries:
            
            tk.Label(new_window, text = entry).pack()
            info_entry = tk.Entry(new_window)
            info_entry.pack()
            self.patient_entries[entry] = info_entry
        
        tk.Button(new_window, text = "Add", command = lambda: self.call_add_patient(info_entry.get())).pack()

    def call_add_patient(self, patientID):
        values = {key: entry.get() for key, entry in self.patient_entries.items()}

        patientID = values["Patient ID"]
        gender = values["Gender"]
        race = values["Race"]
        ethnicity = values["Ethnicity"]
        age = values["Age"]
        zip_code = values["Zip Code"]
        insurance = values["Insurance"]
        complaint = values["Complaint"]
        
        add_patient_data(self.patients_data, patientID, self.notes_data, gender, race, ethnicity, age, zip_code, insurance, complaint)
        messagebox.showinfo("Success", "Patient "+ {values['Patient ID']} + " added.")


# create window for removing patient
    def remove_patient_ui(self):
        new_window = tk.Toplevel()
        new_window.title("Remove Patient")
        
        tk.Label(new_window, text = "Enter Patient ID:").pack()
        patientID_entry = tk.Entry(new_window)
        patientID_entry.pack()
        
        tk.Button(new_window, text = "Remove", command = lambda: self.call_remove_patient(patientID_entry.get(), new_window)).pack()

    def call_remove_patient(self, patientID, new_window):
        if remove_patient_data(self.patients_data, patientID, 'Final_data.csv'):
            messagebox.showinfo("Removed", "Patient ID " + patientID + " data has been successfully removed from the file.")
            new_window.destroy()
        else:
            messagebox.showinfo("Error", "Patient "+ patientID + " could not be removed.")


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
                for visit in patient.records:
                    visit_frame = tk.Frame(details_window)
                    visit_frame.pack(pady = 5)
                    
                    tk.Label(visit_frame, text = ("Visit ID: " + visit.visit_id)).pack()
                    tk.Label(visit_frame, text = ("Department: " + visit.department)).pack()
                    tk.Label(visit_frame, text = ("Date of Visit: " + visit.visit_time)).pack()
                    tk.Label(visit_frame, text = ("Chief Complaint: " + visit.chief_complaint)).pack()
                    tk.Label(visit_frame, text = ("Gender: "+ visit.gender)).pack()
                    tk.Label(visit_frame, text = ("Race: " + visit.race)).pack()
                    tk.Label(visit_frame, text = ("Ethnicity: " + visit.ethnicity)).pack()
                    tk.Label(visit_frame, text = ("Age: " + str(visit.age))).pack()
                    tk.Label(visit_frame, text = ("Zip Code: "+ visit.zip_code)).pack()
                    tk.Label(visit_frame, text = ("Insurance: " + visit.insurance)).pack()

                    if visit.notes:
                        for note in visit.notes:
                            tk.Label(visit_frame, text = ("Note ID: " + str(note.note_id) + " - " + note.note_text)).pack()

                    # add horizontal line between visits 
                    ttk.Separator(details_window, orient = 'horizontal').pack(fill = 'x', pady = 10)

            else:
                tk.Label(details_window, text = ("No visits recorded for this patient.")).pack()
        else: 
            messagebox.showinfo("Error", "Patient " + patientID + " not found.")
    
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
            else:
                tk.Label(notes_display, text = "No notes found.").pack(pady = 10)

            new_window.destroy()

        tk.Button(new_window, text = "View Notes", command = show_notes).pack()


        
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalUI(root)
    root.mainloop()
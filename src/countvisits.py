import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from patient import Patient
from visit import Visit
from note import Note

def counting_patient_visits(patients_data):
    date_window = tk.Toplevel()
    date_window.title("Enter date for Counting visits")

    tk.Label(date_window, text="Enter date (YYYY-MM-DD):").pack()

# Entry window to get the user input
    date_entry = tk.Entry(date_window)
    date_entry.pack()

    def submit_date():
        input_date = date_entry.get()
        if input_date.lower() == 'exit':
            date_window.destroy()
            return

        if input_date:
            date_checker(input_date, date_window, patients_data)
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid date.")
    
    tk.Button(date_window, text = "Submit", command = submit_date).pack()
    
def date_checker(input_date, date_window, patients_data):
# Check basic format YYYY-MM-DD
    if len(input_date) == 10 and input_date[4] == '-' and input_date[7] == '-':
        count = 0

        for patient in patients_data.values():
            for visit in patient.records:
                visit_date_str = visit.visit_time
                if visit_date_str == input_date:
                    count += 1
                    
        if count > 0:
            messagebox.showinfo("Visit Count", "Total visits on "+ input_date + ": " + str(count))
        else:
            messagebox.showinfo("Visit Count", "No visitations on: " + input_date)
    else:
        messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
        
    date_window.destroy()

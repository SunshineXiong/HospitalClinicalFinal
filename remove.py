import csv
import tkinter as tk
from tkinter import messagebox

from patient import Patient
from visit import Visit
from note import Note


## REMOVE PATIENT
def remove_patient_data(patient_data, patient_id, patient_file):
    if patient_id in patient_data:
        removed_patient = patient_data.pop(patient_id)
        print("Patient ID "+ patient_id + " removed successfully.")

        try:
            with open(patient_file, 'r') as file:
                reader = csv.DictReader(file)
                rows = [row for row in reader if row['Patient_ID'] != patient_id]

            # Write back the updated content without the removed patient's data
            with open(patient_file, 'w', newline='') as file:
                # Adjusted fieldnames to match actual CSV columns
                fieldnames = ['Patient_ID', 'Visit_ID', 'Visit_time', 'Visit_department', 'Gender', 'Race', 'Age', 'Ethnicity', 'Insurance', 'Zip_code', 'Chief_complaint', 'Note_ID', 'Note_type']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            return True 
            
        except Exception as e:
            print("Error updating patient file: "+str(e))

    else:
        return False  # return false if patient does not exist 
    print("\n")
    print(str(len(patient_data))+" patients in the database.")

import csv
import tkinter as tk
from tkinter import messagebox

from patient import Patient
from visit import Visit
from note import Note


## REMOVE PATIENT
def remove_patient_data(patient_data, patient_id, patient_file, note_file):
    if patient_id in patient_data:
        removed_patient = patient_data.pop(patient_id)
        print("Patient ID "+ patient_id + " removed successfully.")
        
        try:
            # REMOVE PATIENT FILE FROM PATIENT_DATA.CSV
            with open(patient_file, 'r') as file:
                reader = csv.DictReader(file)
                rows = [row for row in reader if row['Patient_ID'].strip() != patient_id]

            # Write back the updated content without the removed patient's data
            with open(patient_file, 'w', newline='') as file:
                fieldnames = ['Patient_ID', 'Visit_ID', 'Visit_time', 'Visit_department', 'Race', 'Gender',  'Ethnicity', 'Age','Zip_code','Insurance',  'Chief_complaint', 'Note_ID', 'Note_type']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            
            # REMOVE PATIENT NOTES FROM NOTES.CSV
            with open(note_file, 'r') as file:
                reader = csv.reader(file)
                header = next(reader) 
                rows = [row for row in reader if row[1].strip() != patient_id]

            # Write back the updated content without the removed patient's data
            with open(note_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)
            
            return True 
            
        except Exception as e:
            print("Error updating patient file: "+str(e))

    else:
        return False  # return false if patient does not exist 

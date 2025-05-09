import sys 
import csv 
import os

from patient import Patient
from visit import Visit
from note import Note
from loadingFiles import load_user, load_notes, load_patients

# RETRIEVE MODE 
def retrieve_patient_data(patients, patient_id, output_file):
        if patient_id in patients:
            patient = patients[patient_id]

            try:
                with open(output_file, 'w') as file:
                    fieldnames = ['Patient_ID', 'Visit_ID', 'Visit_Time', 'Department', 'Gender', 'Race', 'Ethnicity', 'Age', 'Insurance', 'Zip_Code', 'Chief_Complaint', 'Note_ID', 'Note_type', 'Note_text']
                    
                    fileWrite = csv.DictWriter(file, fieldnames=fieldnames)
                    
                    # Write header (column names)
                    fileWrite.writeheader()
                
                    # Retrieving and printing patient visit data
                    for visit in patient.records:
                            if choice == 'visits':
                                fileWrite.writerow({
                                    'Patient_ID': patient.patient_id,
                                    'Visit_ID': visit.visit_id,
                                    'Visit_Time': visit.visit_time,
                                    'Department': visit.department,
                                    'Gender': visit.gender,
                                    'Race': visit.race,
                                    'Ethnicity': visit.ethnicity,
                                    'Age': visit.age,
                                    'Insurance': visit.insurance,
                                    'Zip_Code': visit.zip_code,
                                    'Chief_Complaint': visit.chief_complaint,
                                    'Note_ID': '',
                                    'Note_type': '',
                                    'Note_text': ''
                                })
                            
                            elif choice == 'notes':
                                for note in visit.notes:
                                    fileWrite.writerow({
                                        'Patient_ID': patient.patient_id,
                                        'Visit_ID': visit.visit_id,
                                        'Visit_Time': '',
                                        'Department': '',
                                        'Gender': '',
                                        'Race': '',
                                        'Ethnicity': '',
                                        'Age': '',
                                        'Insurance': '',
                                        'Zip_Code': '',
                                        'Chief_Complaint': '',
                                        'Note_ID': note.note_id,
                                        'Note_type': note.note_type,
                                        'Note_text': note.note_text
                                    })
                            
                            elif choice == 'all':
                                if not visit.notes:
                                    fileWrite.writerow({
                                        'Patient_ID': patient.patient_id,
                                        'Visit_ID': visit.visit_id,
                                        'Visit_Time': visit.visit_time,
                                        'Department': visit.department,
                                        'Gender': visit.gender,
                                        'Race': visit.race,
                                        'Ethnicity': visit.ethnicity,
                                        'Age': visit.age,
                                        'Insurance': visit.insurance,
                                        'Zip_Code': visit.zip_code,
                                        'Chief_Complaint': visit.chief_complaint,
                                        'Note_ID': '',
                                        'Note_type': '',
                                        'Note_text': ''
                                    })
                                else:
                                    for note in visit.notes:
                                        fileWrite.writerow({
                                            'Patient_ID': patient.patient_id,
                                            'Visit_ID': visit.visit_id,
                                            'Visit_Time': visit.visit_time,
                                            'Department': visit.department,
                                            'Gender': visit.gender,
                                            'Race': visit.race,
                                            'Ethnicity': visit.ethnicity,
                                            'Age': visit.age,
                                            'Insurance': visit.insurance,
                                            'Zip_Code': visit.zip_code,
                                            'Chief_Complaint': visit.chief_complaint,
                                            'Note_ID': note.note_id,
                                            'Note_type': note.note_type,
                                            'Note_text': note.note_text
                                        })
    
                
                    print("Patient data for " + str(patient_id) + " has been written to "+ output_file)
            
            except Exception as e:
                print("Error writing to file: "+ str(e))
        else:
            print("Patient with ID "+ patient_id +" not found.")



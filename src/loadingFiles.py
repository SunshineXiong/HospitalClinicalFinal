import sys 
import csv 
import os

from patient import Patient
from visit import Visit
from note import Note
from user import User
from datetime import datetime


## for encoding='utf-8' --- https://labex.io/tutorials/python-how-to-handle-python-file-text-encoding-421209

def load_user(file_path):
    users = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['username']
                password = row['password']
                role = row['role']
                users[username] = User(username=username, password=password, role=role)

    except Exception as e:
        print("Error: " + str(e))

    return users

def load_notes(note_path, data_path, patient_data):
    notes = [] 
    try:
        note_type_lookup = {}

        # Build lookup from PA3_data.csv to grab the note_type from there 
        with open(data_path, 'r', encoding='utf-8') as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                note_id = row['Note_ID']
                note_type = row['Note_type']
                if note_id:
                    note_type_lookup[note_id] = note_type
                    
        with open(note_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                note_id = row['Note_ID']
                note_text = row['Note_text']
                patient_id = row['Patient_ID']
                visit_id = row['Visit_ID']


                
                # Find the Visit corresponding to this Note's Visit_ID
                visit = None
                for patient in patient_data.values():
                    for v in patient.records:
                        if v.visit_id == visit_id:
                            visit = v
                            break
                    if visit:
                        break
                        
                if visit:
                    note_type = note_type_lookup.get(note_id, '')  # fallback to empty string if not found

                     # Create a Note object
                    note = Note(note_id=note_id, note_text=note_text, note_type=note_type)
                
                # Associate the note with the visit (assuming Visit class has a 'notes' attribute)
                    visit.notes.append(note)
                    notes.append(note)

                        
    except IOError:
        print("Error: The file " + note_path + " was not found.")
    except Exception as e:
        print("Error loading notes: " + str(e))

    return notes


def load_patients(input_path):
    patients = {}
    
    try:
        print("Loading patient data from " + input_path + "...\n")

        # Load all notes first, grouped by Visit_ID
        notes_by_visit = {}
        with open('PA3_notes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                visit_id = row['Visit_ID']
                note_obj = Note(note_id=row['Note_ID'], note_text=row['Note_text'])
                
                if visit_id not in notes_by_visit:
                    notes_by_visit[visit_id] = []
                
                notes_by_visit[visit_id].append(note_obj)

        with open(input_path, 'r') as file:
            fileReader = csv.DictReader(file)
            
            for row in fileReader:
                patient_id = row['Patient_ID']
                visit_id = row['Visit_ID']
                visit_time = row['Visit_time']

            # Handle format like 3/5/2002 or 12/25/2020
                for date in ['%m/%d/%Y', '%Y-%m-%d']:
                    try:
                        visit_time = datetime.strptime(visit_time, '%m/%d/%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        continue 

                
                department = row['Visit_department']
                gender = row['Gender']
                race = row['Race']
                
                try:
                    age = int(row['Age'])
                except ValueError:
                    print("Bad row found:", row)
                    continue 

                ethnicity = row['Ethnicity']
                insurance = row['Insurance']
                zip_code = row['Zip_code']
                chief_complaint = row['Chief_complaint']
                note_id = row['Note_ID']
                note_type = row['Note_type']

                # Add Patient if not already in dict
                if patient_id not in patients:
                    patients[patient_id] = Patient(patient_id)
                    patients[patient_id].records = []

                # Create Visit object
                visit = Visit(visit_id=visit_id, visit_time=visit_time, department=department, race=race, gender=gender, ethnicity=ethnicity, age=age, zip_code=zip_code, insurance=insurance, chief_complaint=chief_complaint, note_id=note_id, note_type=note_type)

                patients[patient_id].records.append(visit)
                patient_num = len(patients)
        print("Loaded " + str(patient_num) +" patients from the file.")

    except IOError:
        print("Error: The file is inaccessible or there was an I/O issue.")
    except Exception as e:
        print("Error reading file: " + str(e))

    return patients


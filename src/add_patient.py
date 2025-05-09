import sys 
import csv 
import os

from patient import Patient
from visit import Visit
from note import Note
from loadingFiles import load_user, load_notes, load_patients

# ADD MODE 
def add_patient_data(patients_data, patient_id, input_data):
    try: 
        mapped_data = {'Patient_ID': patient_id, 
                       'Visit_ID': generate_unique_visitIDS(patients_data), 
                       'Visit_time': input_data['Visit_time'], 
                       'Visit_department': input_data['Visit_department'], 
                       'Gender': input_data.get('Gender', 'UNKNOWN'),
                       'Race': input_data.get('Race', 'UNKNOWN'), 
                       'Ethnicity': input_data.get('Ethnicity', 'UNKNOWN'), 
                       'Age': input_data.get('Age', 'UNKNOWN'), 
                       'Zip_code': input_data.get('Zip_code', 'UNKNOWN'), 
                       'Insurance': input_data.get('Insurance', 'UNKNOWN'), 
                       'Chief_complaint': input_data['Chief_complaint'], 
                       'Note_ID': input_data['Note_ID'], 
                       'Note_type': input_data['Note_type']
                      }
    except Exception as e:
        print("Error: " + str(e))
        return
        
    if patient_id not in patients_data:
    # Patient doesn't exist, create a new one
        patient = Patient(patient_id)
        patients_data[patient_id] = patient
    
        gender = str(input_data['Gender'])
        race = str(input_data['Race'])
        ethnicity = str(input_data['Ethnicity'])
        age = int(input_data['Age'])
        zip_code = str(input_data['Zip_code'])
        insurance = str(input_data['Insurance'])
    else: 
        patient = patients_data[patient_id]
        information = load_info_preexisting_Patients(patient_id)

        if information: 
            race = str(information['Race'])            
            gender = str(information['Gender'])
            age = int(information['Age'])
            ethnicity = str(information['Ethnicity'])
            zip_code = str(information['Zip_code'])
            insurance = str(information['Insurance'])
        
    visit_id = mapped_data['Visit_ID']
    visit_time = mapped_data['Visit_time']
    department = mapped_data['Visit_department']
    chief_complaint = mapped_data['Chief_complaint']
    note_id = mapped_data['Note_ID']
    note_type = mapped_data['Note_type']
    note_text = input_data['Note_text']

#creates the visit and note objects
    new_visit = Visit(visit_id, visit_time, department, race, gender, ethnicity, age, insurance, zip_code, chief_complaint, note_id, note_type)
    new_note = Note(note_id=note_id, note_type=note_type, note_text=note_text)
    
    patient.add_record(new_visit)

    #adds visit to patient visit
    new_visit.add_note(note_id=note_id, note_type=note_type, note_text=note_text)

#appends visit to CSV file
    append_new_visit('Patient_data.csv', patient_id, new_visit)

#appends note to CSV file
    append_new_note('Notes.csv', patient_id, new_note, new_visit)
    
    print("New visit added for Patient ID: " + patient_id)
    load_patients('Patient_data.csv')


def append_new_visit(input_path, patient_id, new_visit):
    with open(input_path, 'a') as file:
        fileWrite=csv.writer(file)
        
        for note in new_visit.notes:
            fileWrite.writerow([patient_id, new_visit.visit_id, new_visit.visit_time, new_visit.department,new_visit.gender, new_visit.race, new_visit.age, new_visit.ethnicity,  new_visit.zip_code, new_visit.insurance, new_visit.chief_complaint, note.note_id, note.note_type])
        print("\nNew visit data for Patient ID " + patient_id + " has been added successfully.")

def append_new_note(input_path, patient_id, new_note,new_visit):
    next_id = 195
    try: 
         with open(input_path, 'r') as file:
            reader = csv.reader(file)       
            rows = list(reader)
            if rows:
                last_row = rows[-1]
                try:
                    last_index = int(last_row[0])
                    next_id = last_index + 1
                except (ValueError, IndexError):
                    pass 
    except FileNotFoundError:
        pass
            
    with open(input_path, 'a') as file:
        fileWrite=csv.writer(file)
        fileWrite.writerow([next_id, patient_id, new_visit.visit_id, new_note.note_id, new_note.note_text])
        print("\nNew note data for Patient ID " + patient_id + " has been added successfully.")
        
# creates visit ID unique numbers and checks so that it isn't a copy of another ID
def generate_unique_visitIDS(patients_data):
    existing_ids = set() #creating set to track existing IDs

    for patient in patients_data.values():
        for visit in patient.records:
            existing_ids.add(int(visit.visit_id))
    
    #generating number
    new_id = 1 
    while new_id in existing_ids:
        new_id += 1
        
    return str(new_id).zfill(5) 

def load_info_preexisting_Patients(patient_id):
    with open('Patient_data.csv', 'r') as csvfile: 
        reader = csv.DictReader(csvfile)
        for row in reader:
            if str(patient_id).strip() == str(row['Patient_ID']).strip():
                return {
                    'Gender': row['Gender'],
                    'Race': row['Race'],
                    'Ethnicity': row['Ethnicity'],
                    'Age': row['Age'],
                    'Zip_code': row['Zip_code'],
                    'Insurance': row['Insurance']
                }
    return None

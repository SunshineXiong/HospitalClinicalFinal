import sys 
import csv 
import os

from patient import Patient
from visit import Visit, Note
from loadingFiles import load_user, load_notes, load_patients

# ADD MODE 
def add_patient_data(patients_data, patient_id, note_data):
    if patient_id not in patients_data:
        race = get_non_empty_input("Enter race: ")
        gender = get_non_empty_input("Enter gender: ")
        ethnicity = get_non_empty_input("Enter ethnicity: ")
    # Handle missing or invalid Age values
        while True:
            age_input = input("Enter age: ").strip()
            if age_input.isdigit():
                age = int(age_input)
                break
            else:
                print("Invalid input. Please enter a valid number for age.")        
        zip_code = get_non_empty_input("Enter zip code: ")
        insurance = get_non_empty_input("Enter insurance: ")
    # Create new patient object and store
        patient = Patient(patient_id)
        patients_data[patient_id] = patient
    else:
        patient = patients_data[patient_id]
        if patient.records:
            first_visit = patient.records[0]
            race = first_visit.race
            gender = first_visit.gender
            ethnicity = first_visit.ethnicity
            age = first_visit.age
            zip_code = first_visit.zip_code
            insurance = first_visit.insurance
        else:
            # Fall back to prompting if no previous visits exist
            race = get_non_empty_input("Enter race: ")
            gender = get_non_empty_input("Enter gender: ")
            ethnicity = get_non_empty_input("Enter ethnicity: ")
            
            while True:
                age_input = int(input("Enter age: "))
                if age_input.isdigit():
                    age = int(age_input)
                    break
                else:
                    print("Invalid input. Please enter a valid number for age.")   
            
            zip_code = get_non_empty_input("Enter zip code: ")
            insurance = get_non_empty_input("Enter insurance: ")
    
#asks user for information about new visit details
    print("Please enter visit details:")
    visit_time = date_checker()
    
    visit_id = str(generate_unique_visitIDS(patients_data))  #Generate a unique Visit_ID 
    print("Visit ID: " + visit_id)
    
    department = get_non_empty_input("Enter visit department: ")
    chief_complaint = get_non_empty_input("Enter chief complaint: ")

    note_id = get_non_empty_input("Enter note ID: ")
    note_type = get_non_empty_input("Enter note type: ")
    note_text = get_non_empty_input("Enter note text: ")
    
#creates the visit visit
    new_visit = Visit(visit_id, visit_time, department, race, gender, ethnicity, age, insurance, zip_code, chief_complaint, note_id, note_type)

    new_note = Note(note_id=note_id, note_type=note_type, note_text=note_text)


#adds visit to patient visit
    patient.add_record(new_visit)
    print("New visit added for Patient ID: " + patient_id)
    new_visit.add_note(note_id=note_id, note_type=note_type, note_text=note_text)

    
#appends visit to CSV file
    append_new_visit('PA3_data.csv', patient_id, new_visit)

#appends note to CSV file
    append_new_note('PA3_Notes.csv', patient_id, new_note, new_visit)
    

    return load_patients('PA3_data.csv')

## 
def append_new_visit(input_path, patient_id, new_visit):
    with open(input_path, 'a') as file:
        fileWrite=csv.writer(file)
        for note in new_visit.notes:
            fileWrite.writerow([patient_id, new_visit.visit_id, new_visit.visit_time, new_visit.department, new_visit.race, new_visit.gender, new_visit.ethnicity, new_visit.age, new_visit.insurance, new_visit.zip_code, new_visit.chief_complaint, note.note_id, note.note_type])
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
    # source: https://www.w3schools.com/python/ref_string_zfill.asp 
    # will fill the visit id with leading 0s so that it asetheically match csv

## this makes sure that when having users input during adding patients, it's not empty 
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input:
            return user_input
        else:
            print("Input cannot be empty. Please try again.")

def date_checker():
    while True:
        input_date = input("Enter date for visit (YYYY-MM-DD): ").strip()
        
        # Check basic format YYYY-MM-DD
        if len(input_date) == 10 and input_date[4] == '-' and input_date[7] == '-':
            return input_date
        else:
            print("Invalid date format. Please enter the date as YYYY-MM-DD.\n")

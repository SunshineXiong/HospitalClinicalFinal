import csv 

from patient import Patient
from visit import Visit
from note import Note

## VIEWING NOTES 
def view_note(patients_data, patientid, input_date):
    results = []
    
    for patient in patients_data.values():
       if patient.patient_id == patientid:
           for visit in patient.records:  
                if visit.visit_time == str(input_date):
                    for note in visit.notes:
                        note_print = ( "Patient ID: " + patient.patient_id + "\n" + "Visit ID: " + visit.visit_id + "\n" + "Note ID: " + note.note_id + "\n" + "Note Type: " + note.note_type + "\n" + "Note Text:\n" + note.note_text + "\n" + "-" * 40)
                        results.append(note_print)

    return results

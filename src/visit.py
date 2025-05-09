from note import Note

# Represents a patient visit with details such as visit time, department, gender, race, etc. Also handles associated notes for each visit.
class Visit:
    def __init__(self, visit_id, visit_time, department, race, gender, ethnicity, age, insurance, zip_code, chief_complaint, note_id=None, note_type=None):

        # Initializes a visit with the given parameters.
        # If note information is provided, a note will be added to the visit. 
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.department = department
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.chief_complaint = chief_complaint
        self.note_id = note_id  
        self.note_type = note_type
        self.notes = []  # List to hold notes for this record

        
    def add_note(self, note_id, note_type, note_text):
        note = Note(note_id, note_type, note_text)
        self.notes.append(note)

    def get_notes(self):
        return self.notes

from visit import Visit

class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.records = []  # List of records associated with the patient

    def add_record(self, record):
        self.records.append(record)

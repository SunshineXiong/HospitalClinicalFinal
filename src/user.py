import csv

class User:
    def __init__(self,username,password,role=None):
        self.username = username
        self.password = password 
        self.role = role

    def get_role(self):
        return self.role
        
    def authenticate(self, username, password):
        """Authenticate based on credentials from the CSV file"""
        with open('PA3_credentials.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == username and row[2] == password:
                    self.username = row[1]
                    self.password = row[2]
                    self.role = row[3]
                    return True
        return False

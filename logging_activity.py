import csv
from datetime import datetime

def log_usage(user, role, action, result, log_file = 'usage_stats.csv'):
    fieldnames = ['User', 'Role', 'Timestamp', 'Action', 'Result']

    try: 
        with open(log_file, 'r', newline = '') as file:
            firstLine = file.readline()
            fileEmpty = not firstLine
    except FileNotFoundError:
        fileEmpty = True
        
    with open(log_file, 'a', newline ='') as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if fileEmpty:
            writer.writeheader()
            
        writer.writerow({'User': user, 'Role': role, 'Timestamp': now, 'Action': action, 'Result': result})
        

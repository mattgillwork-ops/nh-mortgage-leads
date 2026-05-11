import os
from datetime import datetime

def organize_vault():
    notes_dir = 'notes'
    projects = ['Project A', 'Project B']
    dates = [datetime(2023, 1, 1), datetime(2023, 2, 1)]
    
    for project in projects:
        project_dir = os.path.join(notes_dir, project)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        
        for date in dates:
            date_str = date.strftime('%Y-%m-%d')
            date_dir = os.path.join(project_dir, date_str)
            if not os.path.exists(date_dir):
                os.makedirs(date_dir)
    
    print("Vault structure organized.")

if __name__ == "__main__":
    organize_vault()

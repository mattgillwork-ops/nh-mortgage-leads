import os
import subprocess

def test_template():
    template_path = 'templates/template.md'
    if not os.path.exists(template_path):
        print(f"Template file not found: {template_path}")
        return False
    
    with open(template_path, 'r') as file:
        content = file.read()
    
    required_fields = ['agent_id', 'task_type', 'date', 'tags']
    for field in required_fields:
        if field not in content:
            print(f"Required field missing in template: {field}")
            return False
    
    print("Template test passed.")
    return True

def test_script(script_path, file_path):
    result = subprocess.run(['python', script_path, file_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Script failed with error: {result.stderr}")
        return False
    
    print("Script test passed.")
    return True

def test_organize_vault():
    organize_vault_script = 'scripts/organize_vault.py'
    vault_dir = 'notes'
    
    if not os.path.exists(vault_dir):
        print(f"Vault directory not found: {vault_dir}")
        return False
    
    subprocess.run(['python', organize_vault_script], check=True)
    
    projects = ['Project A', 'Project B']
    dates = [datetime(2023, 1, 1), datetime(2023, 2, 1)]
    
    for project in projects:
        project_dir = os.path.join(vault_dir, project)
        if not os.path.exists(project_dir):
            print(f"Project directory not found: {project_dir}")
            return False
        
        for date in dates:
            date_str = date.strftime('%Y-%m-%d')
            date_dir = os.path.join(project_dir, date_str)
            if not os.path.exists(date_dir):
                print(f"Date directory not found: {date_dir}")
                return False
    
    print("Vault organization test passed.")
    return True

def test_add_backlinks():
    add_backlinks_script = 'scripts/add_backlinks.py'
    test_note_path = 'notes/test_note.md'
    
    if not os.path.exists(test_note_path):
        print(f"Test note file not found: {test_note_path}")
        return False
    
    subprocess.run(['python', add_backlinks_script, test_note_path], check=True)
    
    with open(test_note_path, 'r') as file:
        content = file.read()
    
    if 'Backlinks:' not in content:
        print("Backlinks not added to test note.")
        return False
    
    print("Backlink addition test passed.")
    return True

if __name__ == "__main__":
    tests_passed = True
    
    tests_passed &= test_template()
    tests_passed &= test_script('scripts/update_frontmatter.py', 'notes/test_note.md')
    tests_passed &= test_organize_vault()
    tests_passed &= test_add_backlinks()
    
    if tests_passed:
        print("All tests passed.")
    else:
        print("Some tests failed.")

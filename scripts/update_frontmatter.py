import os
import yaml

def update_frontmatter(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    if content.startswith('---'):
        frontmatter_end = content.find('\n---\n')
        if frontmatter_end != -1:
            frontmatter = content[:frontmatter_end]
            content = content[frontmatter_end + 4:]
        else:
            frontmatter = ''
    else:
        frontmatter = ''
    
    frontmatter_dict = {
        'agent_id': os.getenv('AGENT_ID', ''),
        'task_type': os.getenv('TASK_TYPE', ''),
        'date': os.getenv('DATE', ''),
        'tags': os.getenv('TAGS', '')
    }
    
    new_frontmatter = yaml.dump(frontmatter_dict, allow_unicode=True)
    
    if frontmatter:
        new_frontmatter += '\n---\n'
    
    new_content = new_frontmatter + content
    
    with open(file_path, 'w') as file:
        file.write(new_content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python update_frontmatter.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    update_frontmatter(file_path)

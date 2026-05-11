import os
import re

def add_backlinks(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    links = re.findall(r'\[\[(.*?)\]\]', content)
    backlinks = []
    
    for link in links:
        link_path = os.path.join('notes', link + '.md')
        if os.path.exists(link_path):
            with open(link_path, 'r') as link_file:
                link_content = link_file.read()
                if content not in link_content:
                    backlinks.append(link)
    
    if backlinks:
        backlink_str = '\n\nBacklinks:\n' + '\n'.join([f'- [[{link}]]' for link in backlinks])
        new_content = content + backlink_str
    
        with open(file_path, 'w') as file:
            file.write(new_content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python add_backlinks.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    add_backlinks(file_path)

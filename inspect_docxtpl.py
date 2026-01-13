import docxtpl
import re
import os

def find_regex():
    # Try to find the file
    path = docxtpl.__file__
    print(f"docxtpl path: {path}")
    
    with open(path, 'r') as f:
        content = f.read()
    
    # Look for the regex
    match = re.search(r"row_start_ptrn\s*=\s*re\.compile\((.*?)\)", content, re.DOTALL)
    if match:
        print(f"Row start regex: {match.group(1)}")
    else:
        # Check if it's in another file
        dir_path = os.path.dirname(path)
        print(f"Searching in directory: {dir_path}")
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        match = re.search(r"row_start_ptrn\s*=\s*re\.compile\((.*?)\)", content, re.DOTALL)
                        if match:
                            print(f"Found in {file}: {match.group(1)}")
                            return

if __name__ == "__main__":
    find_regex()

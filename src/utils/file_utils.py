import json
import os

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def get_file_paths(directory, extensions=None):
    file_paths = []
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return file_paths
        
    try:
        for root, _, files in os.walk(directory):
            for filename in files:
                if extensions is None or any(filename.lower().endswith(ext) for ext in extensions):
                    file_paths.append(os.path.join(root, filename))
        return file_paths
    except Exception as e:
        print(f"Error scanning directory {directory}: {e}")
        return file_paths
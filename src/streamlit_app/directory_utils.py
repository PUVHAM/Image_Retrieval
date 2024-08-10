import os
from contextlib import contextmanager

def get_path(root_dir):
    files_path = []
    for class_dir in os.listdir(root_dir):
        class_path = os.path.join(root_dir, class_dir)
        if os.path.isdir(class_path):
            for feature_dir in os.listdir(class_path):
                feature_path = os.path.join(class_path, feature_dir)
                if os.path.isdir(feature_path):
                    for filename in os.listdir(feature_path):
                        file_path = os.path.join(feature_path, filename)
                        files_path.append(file_path)
    return files_path

@contextmanager
def change_directory(new_dir):
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        yield
    finally:
        os.chdir(old_dir)
        
def find_path(start_path, target_name):
    start_path = os.path.abspath(start_path)
    while start_path:
        if os.path.basename(start_path) == target_name:
            return start_path
        parent_path = os.path.dirname(start_path)
        if parent_path == start_path:  
            break
        start_path = parent_path
    return None
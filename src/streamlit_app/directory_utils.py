import os
from contextlib import contextmanager

def get_files_from_dir(directory):
    file_paths = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            file_paths.extend(get_files_from_dir(item_path))
        else:
            file_paths.append(item_path)
    return file_paths

def get_files_path(root_dir):
    files_path = []
    for class_dir in os.listdir(root_dir):
        class_path = os.path.join(root_dir, class_dir)
        if os.path.isdir(class_path):
            files_path.extend(get_files_from_dir(class_path))
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
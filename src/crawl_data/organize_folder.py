import os
import shutil
from collections import defaultdict

def organize(train_dir, test_dir):
    # Create the target directories if they don't exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Initialize a dictionary to hold file paths for each class
    class_files = defaultdict(list)

    # Read the file paths from the text file
    with open('filename.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                # Extract the class name from the path
                parts = line.split('\\')
                class_name = parts[2]  # Structure Dataset/category/class/image.jpg
                class_files[class_name].append(line)
                
    # Move images to the train and test directories
    for class_name, files in class_files.items():
        # Create the train and test directories for the class
        train_class_dir = os.path.join(train_dir, class_name)
        test_class_dir = os.path.join(test_dir, class_name)
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(test_class_dir, exist_ok=True)
        
        # Move 19 images to train and 1 image to test
        for i, file_path in enumerate(files):
            if i == 0:
                shutil.copy(file_path, test_class_dir)
            elif i < 20:
                shutil.copy(file_path, train_class_dir)
            
    print("Dataset organization complete!")
    
if __name__ == "__main__":
    # Define the source and target directories
    source_dir = "Dataset"
    train_dir = "data/train"
    test_dir = "data/test"
    
    organize(test_dir=test_dir, train_dir=train_dir)
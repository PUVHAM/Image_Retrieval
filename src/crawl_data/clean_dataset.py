import os
from PIL import Image

def check_and_preprocess_images(image_dir):
    for root, _, files in os.walk(image_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    # Check if image is smaller than 50x50 pixels
                    if img.size[0] < 50 or img.size[1] < 50:
                        os.remove(file_path)
                        print(f"Deleted {file_path}: \
                              Image too small ({img.size[0]}x{img.size[1]})")
                        continue
                    
                    # Convert non-RGB images to RGB
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                        img.save(file_path)
                        print(f"Converted {file_path} to RGB")
                        
            except Exception as e:
                # If file is not an image, delete it
                os.remove(file_path)
                print(f"Deleted {file_path}: Not an image or corrupted file ({str(e)})")
                
if __name__ == "__main__":
    check_and_preprocess_images('Dataset')       
"""
Create sample directory structure for the project
Run this script to create all necessary folders
"""
import os
from pathlib import Path

def create_project_structure():
    """Create all necessary directories for the project"""
    
    directories = [
        'data/train/clean',
        'data/train/medium',
        'data/train/dirty',
        'data/val/clean',
        'data/val/medium',
        'data/val/dirty',
        'raw_data/clean',
        'raw_data/medium',
        'raw_data/dirty',
        'models',
        'esp32',
        'test_images'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created: {directory}")
    
    # Create placeholder files
    placeholder_files = {
        'raw_data/clean/.gitkeep': '# Place your clean hand images here',
        'raw_data/medium/.gitkeep': '# Place your medium cleanliness hand images here',
        'raw_data/dirty/.gitkeep': '# Place your dirty hand images here',
        'test_images/.gitkeep': '# Place test images here for inference'
    }
    
    for file_path, content in placeholder_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Created: {file_path}")
    
    print("\n[OK] Project structure created successfully!")
    print("\nNext steps:")
    print("1. Place your hand images in raw_data/clean/, raw_data/medium/, raw_data/dirty/")
    print("2. Run: python prepare_data.py")
    print("3. Run: python train_model.py")
    print("4. Run: python convert_to_tflite.py")

if __name__ == '__main__':
    create_project_structure()

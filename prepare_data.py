"""
Data Preparation Script
Organizes images into train/validation folders with proper structure
"""
import os
import shutil
from sklearn.model_selection import train_test_split
from pathlib import Path

def prepare_dataset(source_dir='raw_data', train_dir='data/train', val_dir='data/val', test_size=0.2):
    """
    Prepare dataset by splitting into train and validation sets
    
    Args:
        source_dir: Directory containing subdirectories: clean/, medium/, dirty/
        train_dir: Output directory for training data
        val_dir: Output directory for validation data
        test_size: Fraction of data to use for validation
    """
    categories = ['clean', 'medium', 'dirty']
    
    # Create directories
    for category in categories:
        os.makedirs(f'{train_dir}/{category}', exist_ok=True)
        os.makedirs(f'{val_dir}/{category}', exist_ok=True)
    
    # Process each category
    for category in categories:
        category_path = Path(source_dir) / category
        
        if not category_path.exists():
            print(f"Warning: {category_path} does not exist. Skipping...")
            continue
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        files = [f for f in os.listdir(category_path) 
                if any(f.lower().endswith(ext) for ext in image_extensions)]
        
        if len(files) == 0:
            print(f"Warning: No images found in {category_path}")
            continue
        
        # Split into train and validation
        train_files, val_files = train_test_split(
            files, test_size=test_size, random_state=42
        )
        
        # Copy files
        for f in train_files:
            shutil.copy(
                category_path / f,
                Path(train_dir) / category / f
            )
        
        for f in val_files:
            shutil.copy(
                category_path / f,
                Path(val_dir) / category / f
            )
        
        print(f"{category}: {len(train_files)} train, {len(val_files)} validation")
    
    print("\nData preparation complete!")
    print(f"Training data: {train_dir}")
    print(f"Validation data: {val_dir}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Prepare dataset for training')
    parser.add_argument('--source', type=str, default='raw_data',
                       help='Source directory with clean/medium/dirty subdirectories')
    parser.add_argument('--train', type=str, default='data/train',
                       help='Output directory for training data')
    parser.add_argument('--val', type=str, default='data/val',
                       help='Output directory for validation data')
    parser.add_argument('--test-size', type=float, default=0.2,
                       help='Fraction of data for validation')
    
    args = parser.parse_args()
    prepare_dataset(args.source, args.train, args.val, args.test_size)

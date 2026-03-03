"""
Helper script to organize images into dataset folders
Useful if you have images in one folder and need to organize them
"""
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import json

def organize_from_folder(source_folder, target_base='raw_data'):
    """
    Interactive script to organize images into clean/medium/dirty folders
    
    Args:
        source_folder: Folder containing unorganized images
        target_base: Base directory for organized images
    """
    # Create target directories
    categories = ['clean', 'medium', 'dirty']
    for cat in categories:
        Path(f'{target_base}/{cat}').mkdir(parents=True, exist_ok=True)
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = []
    for ext in image_extensions:
        images.extend(Path(source_folder).glob(f'*{ext}'))
        images.extend(Path(source_folder).glob(f'*{ext.upper()}'))
    
    if not images:
        print(f"No images found in {source_folder}")
        return
    
    print(f"\nFound {len(images)} images")
    print("\nInstructions:")
    print("  Press 'c' for clean")
    print("  Press 'm' for medium")
    print("  Press 'd' for dirty")
    print("  Press 's' to skip")
    print("  Press 'q' to quit")
    print("\nStarting organization...\n")
    
    counts = {cat: 0 for cat in categories}
    
    for i, img_path in enumerate(images, 1):
        print(f"\n[{i}/{len(images)}] {img_path.name}")
        
        # Try to open and display image info
        try:
            img = Image.open(img_path)
            print(f"  Size: {img.size}, Format: {img.format}")
        except Exception as e:
            print(f"  Error opening image: {e}")
        
        while True:
            choice = input("  Category (c/m/d/s/q): ").lower().strip()
            
            if choice == 'q':
                print("\nStopped organizing")
                break
            elif choice == 's':
                print("  Skipped")
                break
            elif choice in ['c', 'm', 'd']:
                category = {'c': 'clean', 'm': 'medium', 'd': 'dirty'}[choice]
                
                # Generate filename
                counts[category] += 1
                new_filename = f"{category}_{counts[category]:04d}{img_path.suffix}"
                target_path = Path(f'{target_base}/{category}/{new_filename}')
                
                # Copy file
                shutil.copy(img_path, target_path)
                print(f"  → Saved to {target_path}")
                break
            else:
                print("  Invalid choice. Use c/m/d/s/q")
        
        if choice == 'q':
            break
    
    print(f"\n\nOrganization complete!")
    print(f"Summary:")
    for cat in categories:
        print(f"  {cat}: {counts[cat]} images")

def batch_rename_images(folder, prefix='image'):
    """
    Rename all images in a folder with sequential numbers
    
    Args:
        folder: Folder containing images
        prefix: Prefix for new filenames
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = []
    for ext in image_extensions:
        images.extend(Path(folder).glob(f'*{ext}'))
        images.extend(Path(folder).glob(f'*{ext.upper()}'))
    
    if not images:
        print(f"No images found in {folder}")
        return
    
    print(f"Renaming {len(images)} images...")
    
    for i, img_path in enumerate(images, 1):
        new_name = f"{prefix}_{i:04d}{img_path.suffix}"
        new_path = img_path.parent / new_name
        
        if new_path.exists():
            print(f"Warning: {new_name} already exists, skipping")
            continue
        
        img_path.rename(new_path)
        print(f"  {img_path.name} → {new_name}")
    
    print("Renaming complete!")

def check_dataset(folder='raw_data'):
    """
    Check dataset statistics and quality
    
    Args:
        folder: Dataset folder (should contain clean/, medium/, dirty/)
    """
    categories = ['clean', 'medium', 'dirty']
    
    print(f"\nDataset Statistics: {folder}")
    print("=" * 50)
    
    total_images = 0
    total_size = 0
    
    for category in categories:
        category_path = Path(folder) / category
        
        if not category_path.exists():
            print(f"\n{category}: ❌ Folder not found")
            continue
        
        # Count images
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        images = []
        for ext in image_extensions:
            images.extend(category_path.glob(f'*{ext}'))
            images.extend(category_path.glob(f'*{ext.upper()}'))
        
        count = len(images)
        total_images += count
        
        # Calculate total size
        size = sum(img.stat().st_size for img in images)
        total_size += size
        
        # Check image dimensions (sample first 5)
        dimensions = []
        for img_path in images[:5]:
            try:
                img = Image.open(img_path)
                dimensions.append(img.size)
            except:
                pass
        
        print(f"\n{category.upper()}:")
        print(f"  Images: {count}")
        print(f"  Size: {size / (1024*1024):.2f} MB")
        if dimensions:
            print(f"  Sample dimensions: {dimensions[0]}")
        
        # Recommendations
        if count < 50:
            print(f"  ⚠️  Warning: Less than 50 images (recommended: 100+)")
        elif count < 100:
            print(f"  ⚠️  Warning: Less than 100 images (recommended: 200+)")
        else:
            print(f"  ✅ Good amount of images")
    
    print("\n" + "=" * 50)
    print(f"TOTAL:")
    print(f"  Images: {total_images}")
    print(f"  Size: {total_size / (1024*1024):.2f} MB")
    
    if total_images < 150:
        print(f"\n⚠️  Warning: Total images less than 150")
        print("   Recommended: 300+ images (100+ per category)")
    elif total_images < 300:
        print(f"\n⚠️  Warning: Total images less than 300")
        print("   Recommended: 600+ images (200+ per category)")
    else:
        print(f"\n✅ Good dataset size!")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Organize and manage image dataset')
    parser.add_argument('command', type=str, choices=['organize', 'rename', 'check'],
                       help='Command to run')
    parser.add_argument('--source', type=str, default='.',
                       help='Source folder (for organize/rename)')
    parser.add_argument('--target', type=str, default='raw_data',
                       help='Target folder (for organize)')
    parser.add_argument('--prefix', type=str, default='image',
                       help='Prefix for renaming')
    parser.add_argument('--folder', type=str, default='raw_data',
                       help='Folder to check (for check command)')
    
    args = parser.parse_args()
    
    if args.command == 'organize':
        organize_from_folder(args.source, args.target)
    elif args.command == 'rename':
        batch_rename_images(args.source, args.prefix)
    elif args.command == 'check':
        check_dataset(args.folder)

"""
Rename images in dataset folders to standard format
Renames images to: clean_001.jpg, dirty_001.jpg, medium_001.jpg
"""
import os
from pathlib import Path
from PIL import Image

def rename_images_in_folder(folder_path, prefix, start_num=1):
    """
    Rename all images in a folder with sequential numbers
    
    Args:
        folder_path: Path to folder containing images
        prefix: Prefix for filenames (e.g., 'clean', 'dirty')
        start_num: Starting number (default: 1)
    
    Returns:
        Number of images renamed
    """
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Folder {folder_path} does not exist!")
        return 0
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG']
    images = []
    for ext in image_extensions:
        images.extend(folder.glob(f'*{ext}'))
    
    if not images:
        print(f"No images found in {folder_path}")
        return 0
    
    # Sort images by name for consistent ordering
    images = sorted(images)
    
    print(f"\nRenaming {len(images)} images in {folder_path}...")
    
    renamed_count = 0
    for i, img_path in enumerate(images, start=start_num):
        # Determine extension (prefer jpg)
        try:
            img = Image.open(img_path)
            # Convert to RGB if needed and save as JPG
            if img.mode != 'RGB':
                img = img.convert('RGB')
            ext = '.jpg'
        except:
            # If can't open, keep original extension
            ext = img_path.suffix.lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                ext = '.jpg'
        
        # Generate new filename
        new_filename = f"{prefix}_{i:04d}{ext}"
        new_path = folder / new_filename
        
        # Skip if already correctly named
        if img_path.name == new_filename:
            continue
        
        # Check if target exists
        if new_path.exists() and new_path != img_path:
            # Find next available number
            j = i + 1
            while (folder / f"{prefix}_{j:04d}{ext}").exists():
                j += 1
            new_filename = f"{prefix}_{j:04d}{ext}"
            new_path = folder / new_filename
        
        try:
            # If image needs conversion, convert it
            if img_path.suffix.lower() != ext or img.mode != 'RGB':
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(new_path, 'JPEG', quality=95)
                # Delete original if different
                if img_path != new_path:
                    img_path.unlink()
            else:
                # Just rename
                img_path.rename(new_path)
            
            renamed_count += 1
            if renamed_count % 50 == 0:
                print(f"  Renamed {renamed_count} images...")
        except Exception as e:
            print(f"  Error renaming {img_path.name}: {e}")
    
    print(f"✅ Renamed {renamed_count} images to {prefix}_####.jpg format")
    return renamed_count

def rename_all_datasets(base_dir='raw_data'):
    """Rename all images in clean, medium, and dirty folders"""
    base = Path(base_dir)
    
    if not base.exists():
        print(f"Base directory {base_dir} does not exist!")
        return
    
    categories = ['clean', 'medium', 'dirty']
    total_renamed = 0
    
    print("="*60)
    print("Renaming Dataset Images")
    print("="*60)
    
    for category in categories:
        folder_path = base / category
        if folder_path.exists():
            count = rename_images_in_folder(folder_path, category)
            total_renamed += count
        else:
            print(f"\n⚠️  Folder {folder_path} does not exist (skipping)")
    
    print("\n" + "="*60)
    print(f"Total images renamed: {total_renamed}")
    print("="*60)
    
    # Show final counts
    print("\nFinal dataset counts:")
    for category in categories:
        folder_path = base / category
        if folder_path.exists():
            images = list(folder_path.glob('*.jpg')) + list(folder_path.glob('*.jpeg'))
            print(f"  {category}: {len(images)} images")
        else:
            print(f"  {category}: 0 images (folder missing)")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Rename dataset images to standard format')
    parser.add_argument('--base-dir', type=str, default='raw_data',
                       help='Base directory containing clean/medium/dirty folders')
    parser.add_argument('--category', type=str, choices=['clean', 'medium', 'dirty'],
                       help='Rename only specific category')
    
    args = parser.parse_args()
    
    if args.category:
        # Rename only one category
        folder_path = Path(args.base_dir) / args.category
        rename_images_in_folder(folder_path, args.category)
    else:
        # Rename all categories
        rename_all_datasets(args.base_dir)

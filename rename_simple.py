"""
Simple script to rename images without PIL dependency
Renames images to: clean_001.jpg, dirty_001.jpg, medium_001.jpg
"""
import os
from pathlib import Path

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
    temp_files = []
    
    # First pass: rename to temporary names to avoid conflicts
    for i, img_path in enumerate(images, start=start_num):
        temp_name = f"__temp_{i:05d}__{img_path.name}"
        temp_path = folder / temp_name
        try:
            img_path.rename(temp_path)
            temp_files.append((temp_path, i))
        except Exception as e:
            print(f"  Error with {img_path.name}: {e}")
    
    # Second pass: rename from temp to final names
    for temp_path, i in temp_files:
        # Determine extension (prefer jpg)
        ext = temp_path.suffix.lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            ext = '.jpg'
        elif ext == '.jpeg':
            ext = '.jpg'
        
        # Generate final filename
        final_filename = f"{prefix}_{i:04d}{ext}"
        final_path = folder / final_filename
        
        try:
            temp_path.rename(final_path)
            renamed_count += 1
            if renamed_count % 50 == 0:
                print(f"  Renamed {renamed_count} images...")
        except Exception as e:
            print(f"  Error renaming {temp_path.name}: {e}")
    
    print(f"[OK] Renamed {renamed_count} images to {prefix}_####.{ext} format")
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
            images = list(folder_path.glob('*.jpg')) + list(folder_path.glob('*.jpeg')) + list(folder_path.glob('*.png'))
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

"""
Quick Start Script - Run this to set up and train your model
"""
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    try:
        import tensorflow as tf
        import numpy as np
        import cv2
        from PIL import Image
        import sklearn
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_data():
    """Check if data directories exist and have images"""
    print("\nChecking data structure...")
    
    categories = ['clean', 'medium', 'dirty']
    raw_data_dir = Path('raw_data')
    
    if not raw_data_dir.exists():
        print("❌ raw_data/ directory not found")
        print("Please create raw_data/clean/, raw_data/medium/, raw_data/dirty/")
        print("And add your hand images to these folders")
        return False
    
    total_images = 0
    for category in categories:
        category_path = raw_data_dir / category
        if category_path.exists():
            images = list(category_path.glob('*.jpg')) + list(category_path.glob('*.png'))
            count = len(images)
            total_images += count
            print(f"  {category}: {count} images")
        else:
            print(f"  {category}: directory not found")
    
    if total_images == 0:
        print("\n❌ No images found in raw_data/")
        print("Please add hand images to raw_data/clean/, raw_data/medium/, raw_data/dirty/")
        return False
    
    if total_images < 100:
        print(f"\n⚠️  Warning: Only {total_images} images found. Recommended: 300+ images")
        print("Model may not perform well with limited data")
    
    print(f"\n✅ Found {total_images} total images")
    return True

def setup_directories():
    """Create necessary directories"""
    print("\nSetting up directories...")
    directories = [
        'data/train', 'data/val',
        'models', 'esp32', 'test_images'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def main():
    """Main quick start function"""
    print("=" * 60)
    print("Hand Cleanliness Detection - Quick Start")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Check data
    has_data = check_data()
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    
    if not has_data:
        print("\n1. COLLECT DATA:")
        print("   - Place hand images in raw_data/clean/, raw_data/medium/, raw_data/dirty/")
        print("   - See DATA_COLLECTION_GUIDE.md for details")
        print("   - Aim for 100+ images per category")
        print("\n2. PREPARE DATA:")
        print("   python prepare_data.py")
        print("\n3. TRAIN MODEL:")
        print("   python train_model.py")
        print("\n4. CONVERT TO TFLITE:")
        print("   python convert_to_tflite.py")
        print("\n5. TEST MODEL:")
        print("   python inference.py path/to/test_image.jpg")
    else:
        print("\n1. PREPARE DATA:")
        print("   python prepare_data.py")
        print("\n2. TRAIN MODEL:")
        print("   python train_model.py --epochs 50")
        print("\n3. CONVERT TO TFLITE:")
        print("   python convert_to_tflite.py")
        print("\n4. TEST MODEL:")
        print("   python inference.py path/to/test_image.jpg")
        print("\n5. DEPLOY TO ESP32:")
        print("   - Open esp32/esp32_hand_sanitizer.ino in Arduino IDE")
        print("   - Upload to ESP32-CAM")
    
    print("\n" + "=" * 60)
    print("For detailed instructions, see README.md")
    print("=" * 60)

if __name__ == '__main__':
    main()

# Quick Reference - Dataset Creation

## 🎯 You DON'T Need MediaPipe!

Just capture images and organize them into folders. That's it!

## 📸 Three Ways to Create Dataset

### Method 1: Web Interface (Easiest) ⭐
1. Upload `capture_images_esp32.ino` to ESP32-CAM
2. Open IP address in browser
3. Click buttons to capture images
4. Download and organize into folders

### Method 2: Serial Commands
1. Upload `capture_images_esp32.ino` to ESP32-CAM
2. Run: `python receive_images.py --port COM3`
3. Type `c`/`m`/`d` in Serial Monitor
4. Images auto-saved to folders

### Method 3: Manual
1. Take photos with any camera
2. Copy to `raw_data/clean/`, `raw_data/medium/`, `raw_data/dirty/`
3. Done!

## 📁 Folder Structure

```
raw_data/
├── clean/     ← Put clean hand images here
├── medium/    ← Put medium cleanliness images here
└── dirty/     ← Put dirty hand images here
```

## 🔢 How Many Images?

- **Minimum**: 50 per category (150 total)
- **Recommended**: 100-200 per category (300-600 total)
- **Ideal**: 200+ per category (600+ total)

## ✅ Quick Commands

```bash
# Check your dataset
python organize_images.py check

# Organize images from a folder
python organize_images.py organize --source /path/to/images

# Receive images from ESP32
python receive_images.py --port COM3

# After collecting, prepare dataset
python prepare_data.py

# Train model
python train_model.py
```

## 📚 Full Guides

- `DATASET_CREATION_GUIDE.md` - Complete dataset creation guide
- `DATA_COLLECTION_GUIDE.md` - What images to capture
- `GETTING_STARTED.md` - Step-by-step instructions

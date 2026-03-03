# Complete Dataset Creation Guide

## 🎯 Overview

You **don't need MediaPipe** or any complex tools! You just need to:
1. Capture images with ESP32-CAM
2. Organize them into folders
3. Label them correctly

This guide shows you **three simple methods** to create your dataset.

---

## Method 1: ESP32-CAM Web Interface (Easiest) ⭐ Recommended

### Setup

1. **Upload the capture script**:
   - Open `capture_images_esp32.ino` in Arduino IDE
   - Update WiFi credentials (SSID and password)
   - Upload to ESP32-CAM

2. **Connect to web interface**:
   - Open Serial Monitor (115200 baud)
   - Note the IP address shown (e.g., `192.168.1.100`)
   - Open that IP in your web browser

3. **Capture images**:
   - Place hand in front of camera
   - Click "Capture Clean Hand" / "Capture Medium Hand" / "Capture Dirty Hand"
   - Images are saved to SD card (if available) or shown on screen
   - Download images from the web interface

4. **Organize images**:
   - Copy downloaded images to:
     - `raw_data/clean/` for clean hands
     - `raw_data/medium/` for medium cleanliness
     - `raw_data/dirty/` for dirty hands

**Advantages:**
- ✅ Visual preview before saving
- ✅ Easy to use
- ✅ See statistics
- ✅ No additional software needed

---

## Method 2: ESP32-CAM via Serial (No WiFi needed)

### Setup

1. **Upload the capture script**:
   - Open `capture_images_esp32.ino` in Arduino IDE
   - Upload to ESP32-CAM
   - Open Serial Monitor (115200 baud)

2. **Run Python receiver script**:
   ```bash
   python receive_images.py --port COM3
   ```
   (Change `COM3` to your port: Windows=`COM3/COM4`, Linux=`/dev/ttyUSB0`, Mac=`/dev/tty.usbserial-*`)

3. **Capture images**:
   - In Serial Monitor, type:
     - `c` or `clean` - Capture clean hand
     - `m` or `medium` - Capture medium hand
     - `d` or `dirty` - Capture dirty hand
   - Images are automatically saved to `raw_data/` folders

**Advantages:**
- ✅ No WiFi needed
- ✅ Automatic organization
- ✅ Works offline

---

## Method 3: Manual Camera + Computer (Most Flexible)

### Setup

1. **Capture images**:
   - Use ESP32-CAM to take photos
   - Save to SD card or transfer via USB
   - Or use any camera/phone in the same setup

2. **Organize manually**:
   - Copy images to folders:
     - `raw_data/clean/` - Clean hand images
     - `raw_data/medium/` - Medium cleanliness images
     - `raw_data/dirty/` - Dirty hand images

3. **Rename files** (optional but helpful):
   - Use consistent naming: `clean_001.jpg`, `clean_002.jpg`, etc.
   - Or: `clean_person1_001.jpg`, `clean_person2_001.jpg`

**Advantages:**
- ✅ Full control
- ✅ Can use any camera
- ✅ Easy to review and organize

---

## 📸 What Images to Capture

### Clean Hands (100+ images)
- **What**: Freshly washed and dried hands
- **Characteristics**: 
  - No visible dirt or stains
  - Clean fingernails
  - Smooth appearance
- **Examples**: After thorough handwashing, hands that haven't touched anything

### Medium Cleanliness (100+ images)
- **What**: Lightly soiled hands
- **Characteristics**:
  - Some visible dust
  - Light stains or discoloration
  - Slight contamination
- **Examples**: After light work, touching clean surfaces, light dust

### Dirty Hands (100+ images)
- **What**: Heavily soiled hands
- **Characteristics**:
  - Visible dirt, mud, or stains
  - Obvious contamination
  - Dark spots or patches
- **Examples**: After gardening, handling soil, visible mud/stains

---

## 🎨 Image Quality Guidelines

### DO:
- ✅ Use consistent camera setup (same distance, angle, lighting)
- ✅ Capture in same conditions as production
- ✅ Include variety: different people, hand positions, lighting
- ✅ Use good lighting (not too dark or bright)
- ✅ Keep background consistent (preferably white/neutral)
- ✅ Capture clear, focused images

### DON'T:
- ❌ Don't use blurry images
- ❌ Don't mix different camera setups
- ❌ Don't use images with different backgrounds
- ❌ Don't include images where hands aren't clearly visible
- ❌ Don't use images with extreme lighting

---

## 📁 Folder Structure

Your dataset should look like this:

```
raw_data/
├── clean/
│   ├── clean_001.jpg
│   ├── clean_002.jpg
│   ├── clean_003.jpg
│   └── ... (100+ images)
├── medium/
│   ├── medium_001.jpg
│   ├── medium_002.jpg
│   └── ... (100+ images)
└── dirty/
    ├── dirty_001.jpg
    ├── dirty_002.jpg
    └── ... (100+ images)
```

---

## 🔢 How Many Images?

### Minimum:
- **50 images per category** (150 total) - Will work but accuracy may be limited

### Recommended:
- **100-200 images per category** (300-600 total) - Good balance

### Ideal:
- **200+ images per category** (600+ total) - Best accuracy

**More images = Better model**, but quality matters more than quantity!

---

## ✅ Quick Checklist

- [ ] ESP32-CAM setup and working
- [ ] Camera at fixed position (same as production)
- [ ] Consistent background
- [ ] Good lighting
- [ ] 100+ clean hand images captured
- [ ] 100+ medium cleanliness images captured
- [ ] 100+ dirty hand images captured
- [ ] Images organized in `raw_data/clean/`, `raw_data/medium/`, `raw_data/dirty/`
- [ ] Images are clear and properly labeled

---

## 🚀 After Collecting Images

Once you have images in `raw_data/` folders:

1. **Prepare dataset**:
   ```bash
   python prepare_data.py
   ```
   This splits your data into training (80%) and validation (20%)

2. **Verify your data**:
   - Check that images are in correct folders
   - Review a few samples from each category
   - Remove any incorrectly labeled images

3. **Start training**:
   ```bash
   python train_model.py --epochs 50
   ```

---

## 💡 Tips for Better Results

1. **Consistency is key**: Use the same camera setup for all images
2. **Variety matters**: Include different people, hand positions, types of dirt
3. **Label correctly**: Double-check that images are in the right folders
4. **Start small**: Begin with 50 images per category, test, then collect more
5. **Iterate**: Train a model, test it, identify weaknesses, collect more data

---

## 🐛 Troubleshooting

### "No images found" error
- Check that images are in `raw_data/clean/`, `raw_data/medium/`, `raw_data/dirty/`
- Ensure images are `.jpg`, `.jpeg`, or `.png` format
- Check file permissions

### Images not saving from ESP32
- Check SD card is inserted (if using SD card method)
- Check Serial connection (if using Serial method)
- Verify WiFi connection (if using web interface)

### Can't find Serial port
- **Windows**: Check Device Manager → Ports (COM & LPT)
- **Linux**: Run `ls /dev/ttyUSB*` or `ls /dev/ttyACM*`
- **Mac**: Run `ls /dev/tty.usbserial-*` or `ls /dev/tty.usbmodem*`

---

## 📚 Summary

**You don't need MediaPipe!** Just:
1. Capture images with ESP32-CAM (or any camera)
2. Organize into `raw_data/clean/`, `raw_data/medium/`, `raw_data/dirty/`
3. Run `python prepare_data.py`
4. Train your model!

The simpler the setup, the better - focus on collecting good, diverse, correctly labeled images!

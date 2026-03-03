# Collect Images from Phone - Complete Guide

## 📱 Overview

You can easily collect hand images using your phone camera and transfer them to your computer. This guide shows you **multiple methods** to do this.

---

## Method 1: USB Cable Transfer (Easiest) ⭐ Recommended

### Step 1: Take Photos on Phone

1. **Set up your phone camera**:
   - Use the same setup as your ESP32-CAM (same distance, background, lighting)
   - Take photos in good lighting
   - Keep background consistent (white/neutral)

2. **Take photos**:
   - **Clean hands**: Take 100+ photos of clean hands
   - **Medium cleanliness**: Take 100+ photos of lightly soiled hands
   - **Dirty hands**: Take 100+ photos of dirty hands

3. **Organize on phone** (optional but helpful):
   - Create folders: `Clean`, `Medium`, `Dirty`
   - Move photos to respective folders as you take them

### Step 2: Transfer to Computer

**Android:**
1. Connect phone to computer via USB cable
2. On phone: Select "File Transfer" or "MTP" mode
3. On computer: Open phone storage
4. Copy photos from phone to computer

**iPhone:**
1. Connect iPhone to computer via USB cable
2. Open Photos app (Windows) or Image Capture (Mac)
3. Select photos and import them

### Step 3: Organize into Dataset

Use the helper script:

```bash
python organize_phone_images.py
```

Or manually:
1. Copy photos to:
   - `raw_data/clean/` for clean hands
   - `raw_data/medium/` for medium cleanliness
   - `raw_data/dirty/` for dirty hands

---

## Method 2: Cloud Storage (Google Drive, Dropbox, etc.)

### Step 1: Upload from Phone

1. **Take photos** on your phone (same as Method 1)
2. **Upload to cloud**:
   - **Google Drive**: Open Google Drive app → Upload → Select photos
   - **Dropbox**: Open Dropbox app → Upload → Select photos
   - **OneDrive**: Open OneDrive app → Upload → Select photos
   - **iCloud**: Photos sync automatically

### Step 2: Download to Computer

1. Open cloud storage on computer
2. Download photos to a temporary folder
3. Run organization script:
   ```bash
   python organize_phone_images.py --source /path/to/downloaded/photos
   ```

---

## Method 3: Email Transfer

### Step 1: Email Photos to Yourself

1. Take photos on phone
2. Select photos → Share → Email
3. Email to yourself (attach photos)

### Step 2: Download Attachments

1. Open email on computer
2. Download all attachments to a folder
3. Run organization script:
   ```bash
   python organize_phone_images.py --source /path/to/downloaded/photos
   ```

---

## Method 4: WiFi Transfer Apps

### Using Apps like:
- **Send Anywhere** (Android/iOS)
- **AirDroid** (Android)
- **AirDrop** (iPhone to Mac)
- **Shareit** (Android/iOS)

### Steps:
1. Install app on phone and computer
2. Take photos on phone
3. Send photos to computer via app
4. Organize using script

---

## Method 5: Direct WiFi Transfer (No App Needed)

### Using Python HTTP Server

1. **On your computer**, run:
   ```bash
   python phone_upload_server.py
   ```
   This starts a web server

2. **On your phone**:
   - Connect to same WiFi network
   - Open browser
   - Go to the IP address shown (e.g., `http://192.168.1.100:8000`)
   - Upload photos directly from browser

3. Photos are automatically organized into folders!

---

## 📸 Tips for Taking Photos with Phone

### DO:
- ✅ Use good lighting (natural light is best)
- ✅ Keep phone steady (use both hands or tripod)
- ✅ Maintain consistent distance (30-50cm from hands)
- ✅ Use consistent background (white poster board works great)
- ✅ Take multiple angles (front, back, sides)
- ✅ Include variety (different people, hand positions)

### DON'T:
- ❌ Don't use flash (creates harsh shadows)
- ❌ Don't take blurry photos
- ❌ Don't change camera distance between photos
- ❌ Don't use different backgrounds
- ❌ Don't take photos in extreme lighting

---

## 🎯 Quick Workflow

1. **Take photos** on phone (100+ per category)
2. **Transfer** to computer (USB/Cloud/Email/WiFi)
3. **Organize** using script:
   ```bash
   python organize_phone_images.py
   ```
4. **Verify** dataset:
   ```bash
   python organize_images.py check
   ```
5. **Prepare** for training:
   ```bash
   python prepare_data.py
   ```

---

## 📁 Folder Structure After Transfer

Your `raw_data/` folder should look like:

```
raw_data/
├── clean/
│   ├── IMG_001.jpg
│   ├── IMG_002.jpg
│   └── ... (100+ images)
├── medium/
│   ├── IMG_101.jpg
│   └── ... (100+ images)
└── dirty/
    ├── IMG_201.jpg
    └── ... (100+ images)
```

---

## 🔧 Helper Scripts

### Organize Phone Images
```bash
python organize_phone_images.py
```
- Interactive script to organize images into clean/medium/dirty
- Shows each image and lets you categorize it
- Automatically renames and organizes

### Check Dataset
```bash
python organize_images.py check
```
- Shows statistics about your dataset
- Checks if you have enough images
- Shows image sizes and dimensions

### Batch Rename
```bash
python organize_images.py rename --source raw_data/clean --prefix clean
```
- Renames all images with sequential numbers
- Makes organization easier

---

## 💡 Pro Tips

1. **Take photos in batches**: Do all clean hands first, then medium, then dirty
2. **Name folders on phone**: Create folders before taking photos
3. **Transfer regularly**: Don't wait until you have 1000 photos
4. **Review as you go**: Check photos on computer and delete bad ones
5. **Use consistent setup**: Same background, lighting, distance for all photos

---

## 🐛 Troubleshooting

### Photos not transferring
- Check USB cable connection
- Enable "File Transfer" mode on Android
- Check phone storage permissions

### Photos in wrong format
- Convert using: `python convert_images.py` (if needed)
- Most phones save as JPG which is fine

### Too many photos to organize
- Use batch organization: `python organize_phone_images.py --batch`
- Organize by date/folder if you organized on phone

---

## ✅ Checklist

- [ ] Taken 100+ clean hand photos on phone
- [ ] Taken 100+ medium cleanliness photos on phone
- [ ] Taken 100+ dirty hand photos on phone
- [ ] Transferred photos to computer
- [ ] Organized photos into `raw_data/clean/`, `raw_data/medium/`, `raw_data/dirty/`
- [ ] Verified dataset: `python organize_images.py check`
- [ ] Ready to train: `python prepare_data.py`

---

**Remember**: Phone cameras are often better than ESP32-CAM! Just make sure to match the setup (distance, background, lighting) as closely as possible to your production environment.

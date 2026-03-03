# Quick Start - Upload Images from Phone

## 🚀 Fastest Method: Web Upload (Recommended)

### Step 1: Start Server on Computer

```bash
python phone_upload_server.py
```

You'll see:
```
Server running on:
  Network: http://192.168.1.100:8000
```

### Step 2: Open on Phone

1. Make sure phone is on **same WiFi** as computer
2. Open browser on phone
3. Go to: `http://192.168.1.100:8000` (use the IP shown)
4. Select images → Choose category → Upload!

**Done!** Images are automatically saved to `raw_data/clean/`, `raw_data/medium/`, or `raw_data/dirty/`

---

## 📱 Alternative: USB Transfer

### Step 1: Transfer Photos

1. Connect phone to computer via USB
2. Copy photos from phone to a folder on computer
3. Run organization script:

```bash
python organize_phone_images.py --source /path/to/photos
```

### Step 2: Organize Images

- **GUI Mode** (default): Shows each image, click Clean/Medium/Dirty buttons
- **CLI Mode**: Type `c`/`m`/`d` for each image

---

## ☁️ Cloud Method

1. Upload photos to Google Drive/Dropbox from phone
2. Download to computer
3. Run: `python organize_phone_images.py --source /path/to/downloads`

---

## ✅ After Uploading

Check your dataset:
```bash
python organize_images.py check
```

Prepare for training:
```bash
python prepare_data.py
```

Train model:
```bash
python train_model.py
```

---

**That's it!** See `PHONE_TO_DATASET_GUIDE.md` for detailed instructions.

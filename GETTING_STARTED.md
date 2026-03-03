# Getting Started - Complete Guide

## 🎯 What You Have

A complete machine learning pipeline for hand cleanliness detection with ESP32 integration:

1. **Data Preparation**: Scripts to organize your images
2. **Model Training**: CNN model for 3-class classification (clean/medium/dirty)
3. **Model Conversion**: Convert to TensorFlow Lite for ESP32
4. **Inference**: Test your model on new images
5. **ESP32 Code**: Arduino sketch for camera capture and sanitizer control

## 📋 Step-by-Step Instructions

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- TensorFlow 2.13+
- NumPy, OpenCV, Pillow
- scikit-learn, matplotlib

### Step 2: Collect Your Dataset

**This is the most important step!**

1. **Create folders** (already created):
   - `raw_data/clean/` - Clean hand images
   - `raw_data/medium/` - Moderately dirty hands
   - `raw_data/dirty/` - Dirty hands

2. **Capture images** using your ESP32-CAM:
   - Use the same camera setup as production
   - Aim for **100-200+ images per category**
   - Vary lighting, people, hand positions
   - Keep background and distance consistent

3. **Label correctly**:
   - **Clean**: Freshly washed, no visible dirt
   - **Medium**: Light dust/stains, moderate contamination
   - **Dirty**: Heavy dirt, mud, obvious stains

**See `DATA_COLLECTION_GUIDE.md` for detailed instructions.**

### Step 3: Prepare Dataset

Split your data into training (80%) and validation (20%):

```bash
python prepare_data.py
```

This will:
- Copy images from `raw_data/` to `data/train/` and `data/val/`
- Maintain folder structure (clean/medium/dirty)
- Split randomly but consistently

### Step 4: Train the Model

Train your CNN model:

```bash
python train_model.py --epochs 50 --batch-size 32
```

**Options:**
- `--epochs`: Number of training epochs (default: 50)
- `--batch-size`: Batch size (default: 32)
- `--image-size`: Image size (default: 224)
- `--model-type`: `lightweight` (default) or `standard`

**What happens:**
- Model trains on your data
- Saves best model to `models/best_model.h5`
- Saves final model to `models/final_model.h5`
- Creates training history plot

**Training time:** Depends on dataset size (typically 30 minutes to 2 hours)

### Step 5: Convert to TensorFlow Lite

Convert the trained model for ESP32:

```bash
python convert_to_tflite.py --model models/best_model.h5
```

This creates:
- `models/hand_cleanliness.tflite` - Quantized model (~2-5 MB)
- `esp32/hand_cleanliness_model.h` - C header for Arduino

### Step 6: Test Your Model

Test on a single image:

```bash
python inference.py path/to/image.jpg
```

Or use TFLite model:

```bash
python inference.py path/to/image.jpg --model models/hand_cleanliness.tflite --tflite
```

**Output shows:**
- Predicted class (clean/medium/dirty)
- Confidence score
- Cleanliness score (0-100)
- Recommended dispense time

### Step 7: Deploy to ESP32

1. **Install Arduino IDE** with ESP32 support:
   - Add board URL: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
   - Install "ESP32" board package

2. **Install TensorFlow Lite for Microcontrollers**:
   - Follow: https://www.tensorflow.org/lite/microcontrollers
   - This requires additional setup

3. **Update ESP32 code**:
   - Open `esp32/esp32_hand_sanitizer.ino`
   - Update WiFi credentials (optional)
   - Update pin numbers if needed
   - Include `hand_cleanliness_model.h` (generated in step 5)

4. **Hardware connections**:
   - ESP32-CAM: Camera already integrated
   - Pump: Connect to GPIO 12 via relay/MOSFET
   - Power: 5V for ESP32, 12V for pump

5. **Upload and test**:
   - Select ESP32 board in Arduino IDE
   - Upload sketch
   - Open serial monitor (115200 baud)
   - Place hand in front of camera

## 🔧 Customization

### Adjust Dispense Times

Edit `calculateDispenseTime()` in:
- `inference.py` (Python testing)
- `esp32/esp32_hand_sanitizer.ino` (Arduino)

Current mapping:
- Score 0-30: 3 seconds (very dirty)
- Score 31-60: 2 seconds (medium)
- Score 61-85: 1 second (light)
- Score 86-100: 0 seconds (clean)

### Change Model Architecture

Edit `train_model.py`:
- Modify `create_lightweight_model()` function
- Adjust layers, filters, dropout rates
- Change image size

### Modify Data Augmentation

Edit `train_model.py`:
- Adjust `ImageDataGenerator` parameters
- Add/remove augmentation techniques

## 📊 Expected Results

### Model Performance
- **Training accuracy**: 85-95% (depends on data quality)
- **Validation accuracy**: 80-90% (should be close to training)
- **Model size**: 2-5 MB (quantized)

### Inference Speed
- **Python (CPU)**: ~0.1-0.5 seconds per image
- **ESP32**: 1-3 seconds per image (depends on model size)

## 🐛 Troubleshooting

### "No images found" error
- Check that images are in `raw_data/clean/`, `raw_data/medium/`, `raw_data/dirty/`
- Ensure images are .jpg, .jpeg, or .png format

### Model accuracy is low
- Collect more training data (aim for 500+ images per category)
- Ensure images match production conditions
- Check that labels are correct
- Try training for more epochs

### ESP32 runs out of memory
- Use quantized INT8 model (already enabled)
- Reduce model size in `train_model.py`
- Consider running inference on external device (Raspberry Pi, PC)

### Camera not working
- Check ESP32-CAM wiring
- Verify camera initialization in serial monitor
- Try different frame sizes in code

## 📚 File Reference

- `prepare_data.py` - Organize and split dataset
- `train_model.py` - Train CNN model
- `convert_to_tflite.py` - Convert to TFLite format
- `inference.py` - Test model on images
- `esp32/esp32_hand_sanitizer.ino` - ESP32 Arduino code
- `quick_start.py` - Check setup and show next steps
- `DATA_COLLECTION_GUIDE.md` - Detailed data collection instructions
- `README.md` - Complete project documentation

## 🎓 Learning Resources

- TensorFlow Lite: https://www.tensorflow.org/lite
- ESP32-CAM: https://github.com/espressif/esp32-camera
- Arduino ESP32: https://docs.espressif.com/projects/arduino-esp32/

## ✅ Checklist

Before you start:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] ESP32-CAM hardware ready
- [ ] Sanitizer pump and relay/MOSFET ready

Data collection:
- [ ] Collected 100+ clean hand images
- [ ] Collected 100+ medium cleanliness images
- [ ] Collected 100+ dirty hand images
- [ ] Images placed in `raw_data/` folders

Training:
- [ ] Ran `prepare_data.py`
- [ ] Ran `train_model.py`
- [ ] Checked training accuracy (>80%)
- [ ] Converted to TFLite

Deployment:
- [ ] ESP32 code updated with model
- [ ] Hardware connected correctly
- [ ] Tested with real hands
- [ ] Calibrated dispense times

## 🚀 Quick Commands Summary

```bash
# Setup
pip install -r requirements.txt
python quick_start.py

# Data preparation
python prepare_data.py

# Training
python train_model.py --epochs 50

# Conversion
python convert_to_tflite.py

# Testing
python inference.py test_images/your_image.jpg

# ESP32
# Open esp32/esp32_hand_sanitizer.ino in Arduino IDE
# Upload to ESP32-CAM
```

## 💡 Tips for Success

1. **Data quality > quantity**: 100 well-labeled images > 1000 poor images
2. **Match production conditions**: Train with same camera/setup as production
3. **Iterate**: Start with small dataset, test, collect more data, retrain
4. **Monitor training**: Check `models/training_history.png` for overfitting
5. **Test thoroughly**: Test model on various real-world scenarios before deployment

---

**Good luck with your project!** 🎉

For questions or issues, refer to `README.md` or check the code comments.

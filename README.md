# Hand Cleanliness Detection ML Model for ESP32 Sanitizer Dispenser

This project implements a complete machine learning solution for detecting hand cleanliness and automatically dispensing sanitizer based on the cleanliness score. The system uses an ESP32-CAM to capture hand images and a CNN model to classify them into three categories: **clean**, **medium**, and **dirty**.

## 🎯 Project Overview

- **Input**: Hand images captured by ESP32-CAM
- **Processing**: CNN model classifies cleanliness (clean/medium/dirty)
- **Output**: Sanitizer dispense time based on cleanliness score
  - Score 0-30: 3 seconds (very dirty)
  - Score 31-60: 2 seconds (medium dirty)
  - Score 61-85: 1 second (lightly soiled)
  - Score 86-100: 0 seconds (already clean)

## 📁 Project Structure

```
MDP_ML_MODEL/
├── data/
│   ├── train/
│   │   ├── clean/
│   │   ├── medium/
│   │   └── dirty/
│   └── val/
│       ├── clean/
│       ├── medium/
│       └── dirty/
├── models/
│   ├── best_model.h5          # Best model during training
│   ├── final_model.h5          # Final trained model
│   ├── hand_cleanliness.tflite # TensorFlow Lite model for ESP32
│   └── training_history.png    # Training curves
├── esp32/
│   ├── esp32_hand_sanitizer.ino # ESP32 Arduino code
│   └── hand_cleanliness_model.h # Model as C header (generated)
├── raw_data/                   # Your original images (create this)
│   ├── clean/
│   ├── medium/
│   └── dirty/
├── prepare_data.py             # Data preparation script
├── train_model.py              # Model training script
├── convert_to_tflite.py        # Model conversion script
├── inference.py                # Inference/testing script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Dataset

You need to collect hand images and organize them into three categories:

1. **Create folder structure:**
   ```
   raw_data/
   ├── clean/      # Images of clean hands
   ├── medium/     # Images of moderately dirty hands
   └── dirty/      # Images of dirty hands
   ```

2. **Collect images:**
   - Use your ESP32-CAM to capture images in the same setup as production
   - Aim for at least **100-200 images per category** (more is better)
   - Vary lighting, angles, skin tones, and hand positions
   - Ensure consistent background and camera distance

3. **Prepare dataset:**
   ```bash
   python prepare_data.py --source raw_data --train data/train --val data/val
   ```
   This will split your data into training (80%) and validation (20%) sets.

### 3. Train the Model

```bash
python train_model.py --train-dir data/train --val-dir data/val --epochs 50 --batch-size 32
```

**Options:**
- `--epochs`: Number of training epochs (default: 50)
- `--batch-size`: Batch size (default: 32)
- `--image-size`: Image size (default: 224)
- `--model-type`: `standard` or `lightweight` (default: lightweight)

The model will be saved to `models/best_model.h5` and `models/final_model.h5`.

### 4. Convert to TensorFlow Lite

```bash
python convert_to_tflite.py --model models/best_model.h5 --output models/hand_cleanliness.tflite
```

This creates:
- `models/hand_cleanliness.tflite` - Quantized model for ESP32
- `esp32/hand_cleanliness_model.h` - C header file for Arduino

### 5. Test the Model

Test on a single image:
```bash
python inference.py path/to/image.jpg --model models/best_model.h5
```

Or use TFLite model:
```bash
python inference.py path/to/image.jpg --model models/hand_cleanliness.tflite --tflite
```

### 6. Deploy to ESP32

1. **Install Arduino IDE** with ESP32 support:
   - Add ESP32 board URL: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
   - Install "ESP32" board package

2. **Install TensorFlow Lite for Microcontrollers:**
   - This requires additional setup. See [TFLite Micro documentation](https://www.tensorflow.org/lite/microcontrollers)

3. **Update ESP32 code:**
   - Open `esp32/esp32_hand_sanitizer.ino` in Arduino IDE
   - Update WiFi credentials (optional)
   - Update pin definitions if your hardware differs
   - Include the generated `hand_cleanliness_model.h` header

4. **Upload to ESP32:**
   - Select your ESP32 board
   - Upload the sketch

## 🔧 Hardware Setup

### Required Components:
- ESP32-CAM module
- Sanitizer pump (12V DC pump recommended)
- Relay module or MOSFET (to control pump)
- Power supply (5V for ESP32, 12V for pump)
- Optional: LED indicator

### Connections:
- **Camera**: Already integrated in ESP32-CAM
- **Pump**: Connect to GPIO 12 via relay/MOSFET
- **LED**: Built-in LED on GPIO 4

### Wiring Example:
```
ESP32-CAM          Relay Module          Pump
GPIO 12    --->    IN
                     COM  --->  Pump Positive
                     NO   --->  12V Power Supply
GND        --->    GND
                     Pump Negative ---> GND
```

## 📊 Model Architecture

The model uses a lightweight CNN architecture optimized for ESP32:

- **Input**: 224x224x3 RGB images
- **Architecture**: 
  - 4 convolutional blocks with batch normalization
  - Global average pooling (reduces parameters)
  - 2 dense layers with dropout
  - Output: 3 classes (clean, medium, dirty)
- **Size**: ~2-5 MB (quantized)

## 🎛️ Customization

### Adjust Dispense Times

Edit the `calculateDispenseTime()` function in:
- `inference.py` (Python)
- `esp32_hand_sanitizer.ino` (Arduino)

### Change Cleanliness Thresholds

Modify the score ranges in `calculateDispenseTime()`:
```python
if cleanliness_score < 30:      # Very dirty
    return 3000  # 3 seconds
elif cleanliness_score < 60:    # Medium dirty
    return 2000  # 2 seconds
# etc.
```

### Model Parameters

Edit `train_model.py` to:
- Change model architecture
- Adjust learning rate
- Modify data augmentation
- Change image size

## 📈 Training Tips

1. **More data = better model**: Aim for 500+ images per category
2. **Consistent setup**: Capture training images in the same conditions as production
3. **Data augmentation**: Already included in training script
4. **Monitor training**: Check `models/training_history.png` for overfitting
5. **Early stopping**: Model automatically stops if validation loss doesn't improve

## 🐛 Troubleshooting

### Model not accurate enough:
- Collect more training data
- Ensure training images match production conditions
- Try adjusting model architecture or training parameters

### ESP32 runs out of memory:
- Use quantized INT8 model (already enabled)
- Reduce model size (fewer layers)
- Consider running inference on external device

### Camera not working:
- Check camera wiring
- Verify camera initialization in serial monitor
- Try different frame sizes

### Pump not dispensing:
- Check relay/MOSFET wiring
- Verify GPIO pin number matches your setup
- Test pump directly with power supply

## 📝 Notes

- **Model Size**: The quantized TFLite model should be <5MB for ESP32
- **Inference Time**: Expect 1-3 seconds per inference on ESP32
- **Power**: Ensure adequate power supply for both ESP32 and pump
- **Safety**: Add timeout/error handling for production use

## 🔗 Resources

- [TensorFlow Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers)
- [ESP32-CAM Documentation](https://github.com/espressif/esp32-camera)
- [Arduino ESP32 Setup](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html)

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to improve the model, add features, or optimize for your specific hardware setup!

---

**Important**: You must collect your own dataset of hand images labeled as clean/medium/dirty. The model quality depends entirely on your training data quality and quantity.

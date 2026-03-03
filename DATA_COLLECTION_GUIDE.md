# Data Collection Guide

## Overview

To train an accurate hand cleanliness detection model, you need to collect and label hand images in three categories: **clean**, **medium**, and **dirty**.

## Data Collection Requirements

### Minimum Dataset Size
- **Clean hands**: 100-200 images
- **Medium cleanliness**: 100-200 images  
- **Dirty hands**: 100-200 images
- **Total**: 300-600 images minimum (more is better!)

### Image Quality Guidelines

1. **Use ESP32-CAM**: Capture images with the same camera and setup you'll use in production
2. **Consistent Setup**:
   - Fixed camera height and distance
   - Consistent background (preferably white/neutral)
   - Similar lighting conditions
   - Same hand position/orientation

3. **Image Diversity**:
   - Different people (various skin tones, hand sizes)
   - Different lighting conditions (but consistent per session)
   - Slight variations in hand position
   - Different types of dirt/contamination

## Category Definitions

### Clean (Score: 86-100)
- Freshly washed and dried hands
- No visible dirt, stains, or contamination
- Clean fingernails
- Smooth, clean appearance

**Examples**: Hands after thorough washing, hands that haven't touched anything dirty

### Medium (Score: 41-85)
- Lightly soiled hands
- Some visible dust or light stains
- Slight discoloration
- May have touched surfaces but not heavily contaminated

**Examples**: Hands after light work, hands with light dust, hands that touched clean surfaces

### Dirty (Score: 0-40)
- Heavily soiled hands
- Visible dirt, mud, or stains
- Obvious contamination
- Dark spots or patches

**Examples**: Hands after gardening, hands with visible mud, hands after handling dirty objects

## Collection Process

### Step 1: Setup ESP32-CAM

1. Mount ESP32-CAM at fixed position (e.g., 30-50cm above hand placement area)
2. Set up consistent background (white poster board works well)
3. Ensure good, consistent lighting
4. Test camera capture and save images

### Step 2: Capture Clean Hands

1. Have multiple people wash hands thoroughly
2. Dry hands completely
3. Place hands in camera frame
4. Capture 100-200 images
5. Save to `raw_data/clean/` folder

### Step 3: Capture Medium Cleanliness

1. Have people do light activities (touch clean surfaces, light work)
2. Capture hands with light dust/stains
3. Ensure hands are visibly soiled but not heavily dirty
4. Capture 100-200 images
5. Save to `raw_data/medium/` folder

### Step 4: Capture Dirty Hands

1. Have people do dirty activities (gardening, handling soil, etc.)
2. Ensure visible contamination
3. Capture various types of dirt (mud, dust, stains)
4. Capture 100-200 images
5. Save to `raw_data/dirty/` folder

## Image Naming Convention

Use descriptive names:
- `clean_001.jpg`, `clean_002.jpg`, etc.
- `medium_001.jpg`, `medium_002.jpg`, etc.
- `dirty_001.jpg`, `dirty_002.jpg`, etc.

Or include metadata:
- `clean_person1_001.jpg`
- `medium_person2_001.jpg`
- `dirty_person3_001.jpg`

## Quick Collection Script for ESP32

You can modify the ESP32 code to save images directly:

```cpp
// Add this function to capture and save images
void saveImageToSD() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (fb) {
    // Save to SD card or send via serial/USB
    // Format: clean_001.jpg, medium_001.jpg, dirty_001.jpg
  }
  esp_camera_fb_return(fb);
}
```

## Alternative: Use Existing Hand Images

If you have access to hand images from other sources:

1. **Filter for hand images**: Extract images containing hands
2. **Manually label**: Review each image and categorize as clean/medium/dirty
3. **Resize to match**: Ensure images are similar size/resolution to ESP32 captures
4. **Augment**: Use data augmentation during training to increase diversity

## Data Validation

Before training, verify your dataset:

1. **Check distribution**: Ensure roughly equal numbers in each category
2. **Review samples**: Manually check that labels are correct
3. **Remove bad images**: Delete blurry, incorrectly labeled, or irrelevant images
4. **Test split**: Ensure train/val split maintains class balance

## Tips for Better Results

1. **More data = better model**: Aim for 500+ images per category if possible
2. **Consistent conditions**: Keep camera setup identical to production
3. **Real-world variety**: Include edge cases (very clean, very dirty)
4. **Regular updates**: Retrain with new data as you collect more images
5. **Validation set**: Keep 20% of data separate for validation (don't use for training)

## Troubleshooting

### Not enough images?
- Use data augmentation (already included in training script)
- Collect more images over time
- Consider transfer learning from pre-trained models

### Model not accurate?
- Check if training images match production conditions
- Ensure labels are correct
- Collect more diverse examples
- Adjust model architecture or training parameters

### Unbalanced classes?
- Collect more images for underrepresented classes
- Use class weights in training (can be added to training script)

---

**Remember**: The quality of your training data directly determines your model's accuracy. Spend time collecting good, diverse, correctly labeled images!

# Sources for Medium Cleanliness Hand Images

## 🎯 Overview

You need images of **medium cleanliness hands** - hands that are lightly soiled, have some dust, or moderate contamination (between clean and dirty).

## 📸 Best Approach: Create Your Own

**Recommended**: Take 100-200 photos yourself of hands with:
- Light dust or soil
- Partial dirt on fingertips
- Slight discoloration
- Light grease or food residue
- Hands after light work (not heavily soiled)

This ensures consistency with your clean/dirty images.

---

## 🌐 Online Image Sources

### 1. Free Stock Photo Sites (Search for "hands")

**Unsplash** (Free, high quality)
- URL: https://unsplash.com/s/photos/hands
- Search terms: "hands", "dirty hands", "soiled hands", "working hands"
- License: Free to use (even commercially)
- How to use: Download images showing moderately dirty hands

**Pexels** (Free)
- URL: https://www.pexels.com/search/hands/
- Search terms: "hands", "dirty hands", "worker hands"
- License: Free to use
- Filter: Look for images with light dirt/dust

**Pixabay** (Free)
- URL: https://pixabay.com/images/search/hands/
- Search terms: "hands", "dirty hands", "working hands"
- License: Free to use

### 2. Kaggle Datasets

**Hand Gesture Recognition Datasets**
- Search: https://www.kaggle.com/datasets
- Search terms: "hand", "hand gesture", "hand images"
- Some datasets contain hand images you can filter for medium cleanliness

**Note**: Most hand datasets focus on gestures, not cleanliness levels. You'll need to manually review and select images that show medium cleanliness.

### 3. Google Images (Use with Caution)

- Search: "lightly soiled hands", "moderately dirty hands", "hands with dust"
- **Important**: Check image licenses before using
- Filter by "Usage Rights" → "Labeled for reuse"

### 4. Research Datasets

**IEEE DataPort - Handwashing Dataset**
- URL: https://ieee-dataport.org/documents/handwashing-dataset-based-who-prescribed-handwashing-steps
- Contains hand images at different stages
- Some intermediate stages might work for "medium" category
- Requires registration

**GitHub - HandWash Project**
- URL: https://github.com/huiwen99/HandWash
- Contains hand images from handwashing steps
- May have intermediate cleanliness levels

---

## 🎨 What to Look For in Medium Images

### Characteristics of Medium Cleanliness:
- ✅ Some visible dust or light soil
- ✅ Partial dirt on fingertips or palms
- ✅ Slight discoloration (not completely clean, not heavily dirty)
- ✅ Light grease or food residue
- ✅ Hands that have touched surfaces but aren't heavily contaminated

### Avoid:
- ❌ Completely clean hands (belongs in clean category)
- ❌ Heavily soiled hands (belongs in dirty category)
- ❌ Hands with extreme dirt/mud (too dirty)
- ❌ Blurry or unclear images

---

## 📥 How to Download and Organize

### Method 1: Manual Download
1. Visit the websites above
2. Search for appropriate images
3. Download to a temporary folder
4. Review each image
5. Copy to `raw_data/medium/` folder
6. Run: `python rename_simple.py`

### Method 2: Use Python Script (for bulk downloads)

I can create a script to help download images from Unsplash/Pexels APIs if needed.

---

## 🔄 Alternative: Generate from Your Existing Data

### Option 1: Use Some "Clean" Images
- If some of your "clean" images are borderline (slightly dusty), move them to medium
- Review your clean folder and identify images that aren't perfectly clean

### Option 2: Use Some "Dirty" Images
- If some of your "dirty" images are only moderately dirty, move them to medium
- Review your dirty folder and identify images that aren't heavily soiled

### Option 3: Data Augmentation
- The training script already includes augmentation
- But you still need real medium images for best results

---

## 💡 Recommended Workflow

1. **Take 50-100 photos yourself** of medium cleanliness hands
   - Use same setup as your clean/dirty images
   - Same background, lighting, distance

2. **Download 50-100 images** from free stock photo sites
   - Review each one carefully
   - Ensure they match your definition of "medium"

3. **Review your existing data**
   - Move borderline clean → medium
   - Move borderline dirty → medium

4. **Aim for 200+ medium images** total
   - This balances with your 622 clean and 510 dirty images

---

## ✅ Quick Checklist

- [ ] Collected 50-100 medium images yourself
- [ ] Downloaded 50-100 from stock photo sites
- [ ] Reviewed existing clean/dirty folders for borderline images
- [ ] Total medium images: 200+ (to balance dataset)
- [ ] All images reviewed and properly categorized
- [ ] Run `python rename_simple.py` to standardize names

---

## 🚀 After Collecting Medium Images

1. **Rename all images**:
   ```bash
   python rename_simple.py
   ```

2. **Check dataset**:
   ```bash
   python organize_images.py check
   ```

3. **Prepare for training**:
   ```bash
   python prepare_data.py
   ```

4. **Train model**:
   ```bash
   python train_model.py --epochs 50
   ```

---

**Remember**: Quality over quantity! It's better to have 100 well-labeled medium images than 500 unclear ones. Make sure medium images are clearly distinguishable from both clean and dirty categories.

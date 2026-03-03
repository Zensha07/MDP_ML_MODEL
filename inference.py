"""
Inference script for testing the trained model on new images
"""
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import os
import argparse

def load_model(model_path='models/best_model.h5'):
    """Load the trained Keras model"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found!")
    
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    return model

def load_tflite_model(tflite_path='models/hand_cleanliness.tflite'):
    """Load TensorFlow Lite model"""
    if not os.path.exists(tflite_path):
        raise FileNotFoundError(f"TFLite model {tflite_path} not found!")
    
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    return interpreter

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for inference
    
    Args:
        image_path: Path to image file
        target_size: Target size (height, width)
    
    Returns:
        Preprocessed image array
    """
    # Load image
    if isinstance(image_path, str):
        img = Image.open(image_path)
    else:
        img = image_path
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize
    img = img.resize(target_size)
    
    # Convert to array and normalize
    img_array = np.array(img, dtype=np.float32) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_cleanliness(model, image_path, class_names=['clean', 'medium', 'dirty']):
    """
    Predict cleanliness category and score
    
    Args:
        model: Keras model or TFLite interpreter
        image_path: Path to image file
        class_names: List of class names
    
    Returns:
        Dictionary with predictions
    """
    # Preprocess image
    img_array = preprocess_image(image_path)
    
    # Check if it's TFLite interpreter
    if isinstance(model, tf.lite.Interpreter):
        # Get input/output details
        input_details = model.get_input_details()
        output_details = model.get_output_details()
        
        # Prepare input
        input_data = img_array
        if input_details[0]['dtype'] == np.uint8:
            input_scale, input_zero_point = input_details[0]['quantization']
            input_data = (img_array / input_scale + input_zero_point).astype(np.uint8)
        
        # Run inference
        model.set_tensor(input_details[0]['index'], input_data)
        model.invoke()
        
        # Get output
        output_data = model.get_tensor(output_details[0]['index'])
        
        if output_details[0]['dtype'] == np.uint8:
            output_scale, output_zero_point = output_details[0]['quantization']
            output_data = (output_data.astype(np.float32) - output_zero_point) * output_scale
        
        predictions = output_data[0]
    else:
        # Keras model
        predictions = model.predict(img_array, verbose=0)[0]
    
    # Get predicted class
    predicted_class_idx = np.argmax(predictions)
    predicted_class = class_names[predicted_class_idx]
    confidence = float(predictions[predicted_class_idx])
    
    # Calculate cleanliness score (0-100)
    # Clean = 100, Medium = 50, Dirty = 0
    cleanliness_score = (
        predictions[0] * 100 +  # clean
        predictions[1] * 50 +   # medium
        predictions[2] * 0      # dirty
    )
    
    return {
        'predicted_class': predicted_class,
        'confidence': confidence,
        'cleanliness_score': cleanliness_score,
        'probabilities': {
            class_names[i]: float(predictions[i]) 
            for i in range(len(class_names))
        }
    }

def calculate_dispense_time(cleanliness_score):
    """
    Calculate sanitizer dispense time based on cleanliness score
    
    Args:
        cleanliness_score: Score from 0-100
    
    Returns:
        Dispense time in milliseconds
    """
    if cleanliness_score < 30:
        # Very dirty
        return 3000  # 3 seconds
    elif cleanliness_score < 60:
        # Medium dirty
        return 2000  # 2 seconds
    elif cleanliness_score < 85:
        # Lightly soiled
        return 1000  # 1 second
    else:
        # Already clean
        return 0  # No dispense

def test_image(image_path, model_path='models/best_model.h5', use_tflite=False):
    """Test a single image"""
    if use_tflite:
        model = load_tflite_model(model_path.replace('.h5', '.tflite'))
    else:
        model = load_model(model_path)
    
    result = predict_cleanliness(model, image_path)
    
    print(f"\nImage: {image_path}")
    print(f"Predicted Class: {result['predicted_class']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Cleanliness Score: {result['cleanliness_score']:.2f}/100")
    print("\nProbabilities:")
    for class_name, prob in result['probabilities'].items():
        print(f"  {class_name}: {prob:.2%}")
    
    dispense_time = calculate_dispense_time(result['cleanliness_score'])
    print(f"\nRecommended Dispense Time: {dispense_time}ms ({dispense_time/1000:.1f} seconds)")
    
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test model on images')
    parser.add_argument('image', type=str, help='Path to image file')
    parser.add_argument('--model', type=str, default='models/best_model.h5',
                       help='Path to model file')
    parser.add_argument('--tflite', action='store_true',
                       help='Use TFLite model instead of Keras')
    
    args = parser.parse_args()
    
    if args.tflite:
        model_path = args.model.replace('.h5', '.tflite')
    else:
        model_path = args.model
    
    test_image(args.image, model_path, args.tflite)

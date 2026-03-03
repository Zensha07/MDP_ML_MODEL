"""
Convert Keras model to TensorFlow Lite format for ESP32 deployment
"""
import tensorflow as tf
import numpy as np
import os

def convert_to_tflite(model_path='models/best_model.h5', 
                      output_path='models/hand_cleanliness.tflite',
                      quantize=True):
    """
    Convert Keras model to TensorFlow Lite format
    
    Args:
        model_path: Path to saved Keras model (.h5)
        output_path: Output path for TFLite model
        quantize: Whether to apply quantization for smaller model size
    """
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found!")
    
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if quantize:
        print("Converting with quantization (INT8)...")
        # Quantization-aware conversion
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        
        # Set optimization flags
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        
        # For full integer quantization, provide representative dataset
        def representative_dataset():
            # Use a small sample of training data
            # In practice, you'd load actual images here
            for _ in range(100):
                # Generate random data matching your input shape
                yield [np.random.rand(1, 224, 224, 3).astype(np.float32)]
        
        converter.representative_dataset = representative_dataset
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
        
        try:
            tflite_model = converter.convert()
        except Exception as e:
            print(f"Full quantization failed: {e}")
            print("Falling back to dynamic range quantization...")
            # Fallback to dynamic range quantization
            converter = tf.lite.TFLiteConverter.from_keras_model(model)
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            tflite_model = converter.convert()
    else:
        print("Converting without quantization (FLOAT32)...")
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
    
    # Save TFLite model
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    # Get model size
    model_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    print(f"\nTFLite model saved to {output_path}")
    print(f"Model size: {model_size:.2f} MB")
    
    # Test the TFLite model
    print("\nTesting TFLite model...")
    interpreter = tf.lite.Interpreter(model_path=output_path)
    interpreter.allocate_tensors()
    
    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print(f"Input shape: {input_details[0]['shape']}")
    print(f"Input type: {input_details[0]['dtype']}")
    print(f"Output shape: {output_details[0]['shape']}")
    print(f"Output type: {output_details[0]['dtype']}")
    
    # Test with dummy input
    input_data = np.random.rand(1, 224, 224, 3).astype(np.float32)
    
    if input_details[0]['dtype'] == np.uint8:
        # Quantize input for INT8 model
        input_scale, input_zero_point = input_details[0]['quantization']
        input_data = (input_data / input_scale + input_zero_point).astype(np.uint8)
    
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(f"\nTest output: {output_data}")
    print("TFLite model conversion successful!")
    
    return output_path

def convert_to_c_header(tflite_path='models/hand_cleanliness.tflite',
                        header_path='esp32/hand_cleanliness_model.h'):
    """
    Convert TFLite model to C header file for ESP32
    
    Args:
        tflite_path: Path to TFLite model
        header_path: Output path for C header file
    """
    if not os.path.exists(tflite_path):
        raise FileNotFoundError(f"TFLite model {tflite_path} not found!")
    
    print(f"\nConverting {tflite_path} to C header...")
    
    # Read TFLite model as bytes
    with open(tflite_path, 'rb') as f:
        model_bytes = f.read()
    
    # Create header file
    os.makedirs(os.path.dirname(header_path), exist_ok=True)
    
    header_name = os.path.basename(header_path).upper().replace('.', '_')
    
    with open(header_path, 'w') as f:
        f.write(f"#ifndef {header_name}\n")
        f.write(f"#define {header_name}\n\n")
        f.write("// Auto-generated from TensorFlow Lite model\n")
        f.write(f"// Model size: {len(model_bytes)} bytes\n\n")
        f.write(f"const unsigned char hand_cleanliness_model[] = {{\n")
        
        # Write bytes in hex format
        for i, byte in enumerate(model_bytes):
            if i % 12 == 0:
                f.write("  ")
            f.write(f"0x{byte:02x},")
            if (i + 1) % 12 == 0:
                f.write("\n")
            else:
                f.write(" ")
        
        if len(model_bytes) % 12 != 0:
            f.write("\n")
        
        f.write("};\n")
        f.write(f"const unsigned int hand_cleanliness_model_len = {len(model_bytes)};\n\n")
        f.write(f"#endif // {header_name}\n")
    
    print(f"C header saved to {header_path}")
    print(f"Model array size: {len(model_bytes)} bytes")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert Keras model to TFLite')
    parser.add_argument('--model', type=str, default='models/best_model.h5',
                       help='Input Keras model path')
    parser.add_argument('--output', type=str, default='models/hand_cleanliness.tflite',
                       help='Output TFLite model path')
    parser.add_argument('--no-quantize', action='store_true',
                       help='Disable quantization')
    parser.add_argument('--header', type=str, default='esp32/hand_cleanliness_model.h',
                       help='Output C header path for ESP32')
    
    args = parser.parse_args()
    
    tflite_path = convert_to_tflite(
        model_path=args.model,
        output_path=args.output,
        quantize=not args.no_quantize
    )
    
    if args.header:
        convert_to_c_header(tflite_path, args.header)

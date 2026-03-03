"""
Receive images from ESP32-CAM via Serial and save them to dataset folders
Run this script while ESP32 is sending images via Serial
"""
import serial
import os
from pathlib import Path
import time

def receive_images(port='COM3', baudrate=115200, output_dir='raw_data'):
    """
    Receive images from ESP32-CAM via Serial port
    
    Args:
        port: Serial port (Windows: COM3, COM4, etc. | Linux/Mac: /dev/ttyUSB0, /dev/ttyACM0)
        baudrate: Serial baud rate (default: 115200)
        output_dir: Directory to save images
    """
    # Create output directories
    categories = ['clean', 'medium', 'dirty']
    for category in categories:
        Path(f'{output_dir}/{category}').mkdir(parents=True, exist_ok=True)
    
    # Counters
    counts = {cat: len(list(Path(f'{output_dir}/{cat}').glob('*.jpg'))) for cat in categories}
    
    print(f"Connecting to {port} at {baudrate} baud...")
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected! Waiting for images...")
        print(f"\nCurrent counts:")
        for cat in categories:
            print(f"  {cat}: {counts[cat]}")
        print("\nPress Ctrl+C to stop\n")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        print("\nCommon ports:")
        print("  Windows: COM3, COM4, COM5, etc.")
        print("  Linux: /dev/ttyUSB0, /dev/ttyACM0")
        print("  Mac: /dev/tty.usbserial-*, /dev/tty.usbmodem*")
        return
    
    buffer = b''
    current_category = None
    image_started = False
    
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                buffer += data
                
                # Look for image start marker
                if b'===IMAGE_START:' in buffer:
                    # Extract category
                    start_idx = buffer.find(b'===IMAGE_START:')
                    end_idx = buffer.find(b'===', start_idx + 14)
                    if end_idx != -1:
                        current_category = buffer[start_idx + 14:end_idx].decode('utf-8').strip()
                        buffer = buffer[end_idx + 3:]
                        image_started = True
                        print(f"Receiving {current_category} image...", end='', flush=True)
                
                # Look for image end marker
                if b'===IMAGE_END===' in buffer and image_started:
                    end_idx = buffer.find(b'===IMAGE_END===')
                    image_data = buffer[:end_idx]
                    buffer = buffer[end_idx + 15:]
                    
                    if current_category and current_category in categories:
                        # Save image
                        counts[current_category] += 1
                        filename = f'{output_dir}/{current_category}/{current_category}_{counts[current_category]:04d}.jpg'
                        
                        with open(filename, 'wb') as f:
                            f.write(image_data)
                        
                        print(f" Saved as {filename} ({len(image_data)} bytes)")
                        image_started = False
                        current_category = None
                    else:
                        print(" Error: Unknown category")
                        image_started = False
                
                # Prevent buffer from growing too large
                if len(buffer) > 1000000:  # 1MB
                    print("\nWarning: Buffer overflow, clearing...")
                    buffer = b''
                    image_started = False
                    
    except KeyboardInterrupt:
        print("\n\nStopped receiving images")
        print("\nFinal counts:")
        for cat in categories:
            print(f"  {cat}: {counts[cat]}")
    finally:
        ser.close()
        print("\nSerial port closed")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Receive images from ESP32-CAM via Serial')
    parser.add_argument('--port', type=str, default='COM3',
                       help='Serial port (COM3 for Windows, /dev/ttyUSB0 for Linux)')
    parser.add_argument('--baud', type=int, default=115200,
                       help='Baud rate')
    parser.add_argument('--output', type=str, default='raw_data',
                       help='Output directory')
    
    args = parser.parse_args()
    
    receive_images(args.port, args.baud, args.output)

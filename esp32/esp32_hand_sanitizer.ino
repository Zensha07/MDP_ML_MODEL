/*
 * ESP32 Hand Sanitizer Dispenser with ML Cleanliness Detection
 * 
 * This code captures images from ESP32-CAM, processes them with TensorFlow Lite,
 * and controls a sanitizer pump based on hand cleanliness score.
 * 
 * Hardware Requirements:
 * - ESP32-CAM module
 * - Sanitizer pump (connected via relay/MOSFET to PUMP_PIN)
 * - Optional: LED indicator
 * 
 * Model Requirements:
 * - TensorFlow Lite model converted to C header (hand_cleanliness_model.h)
 */

#include "esp_camera.h"
#include <WiFi.h>
#include "hand_cleanliness_model.h"  // Include your converted model

// ==================== CONFIGURATION ====================
// WiFi credentials (optional - for remote monitoring)
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Camera pins for ESP32-CAM
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// Sanitizer pump control pin
#define PUMP_PIN 12
#define LED_PIN 4  // Built-in LED on ESP32-CAM

// Model configuration
#define MODEL_INPUT_SIZE 224
#define MODEL_INPUT_CHANNELS 3
#define MODEL_OUTPUT_CLASSES 3

// Class names (must match training)
const char* CLASS_NAMES[] = {"clean", "medium", "dirty"};

// ==================== TENSORFLOW LITE SETUP ====================
// Note: You'll need to install TensorFlow Lite for Microcontrollers
// This is a simplified version - full implementation requires TFLM library

// For now, we'll use a placeholder structure
// In production, you'd use actual TFLite Micro library:
// #include <tensorflow/lite/micro/all_ops_resolver.h>
// #include <tensorflow/lite/micro/micro_interpreter.h>

// Placeholder for model inference
// Replace this with actual TFLite Micro inference code
float runInference(uint8_t* image_data) {
  // TODO: Implement actual TFLite Micro inference
  // This is a placeholder that returns dummy values
  
  // For now, return a dummy cleanliness score
  // In production, this would run the actual model
  return 50.0;  // Placeholder
}

// ==================== CAMERA SETUP ====================
bool initCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_RGB565;  // RGB565 for easier processing
  config.frame_size = FRAMESIZE_QVGA;  // 320x240
  config.jpeg_quality = 10;
  config.fb_count = 1;
  
  // Initialize camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return false;
  }
  
  Serial.println("Camera initialized successfully");
  return true;
}

// ==================== IMAGE PREPROCESSING ====================
void preprocessImage(camera_fb_t* fb, uint8_t* output) {
  // Convert RGB565 to RGB888 and resize to 224x224
  // This is a simplified version - you may want to use a proper resizing algorithm
  
  int input_width = fb->width;
  int input_height = fb->height;
  int output_size = MODEL_INPUT_SIZE * MODEL_INPUT_SIZE * MODEL_INPUT_CHANNELS;
  
  // Simple nearest-neighbor resize (for production, use better algorithm)
  for (int y = 0; y < MODEL_INPUT_SIZE; y++) {
    for (int x = 0; x < MODEL_INPUT_SIZE; x++) {
      int src_x = (x * input_width) / MODEL_INPUT_SIZE;
      int src_y = (y * input_height) / MODEL_INPUT_SIZE;
      
      // Read RGB565 pixel
      uint16_t pixel = ((uint16_t*)fb->buf)[src_y * input_width + src_x];
      
      // Convert RGB565 to RGB888
      uint8_t r = ((pixel >> 11) & 0x1F) << 3;
      uint8_t g = ((pixel >> 5) & 0x3F) << 2;
      uint8_t b = (pixel & 0x1F) << 3;
      
      // Normalize to 0-255 (model expects 0-1, but we'll handle quantization)
      int idx = (y * MODEL_INPUT_SIZE + x) * MODEL_INPUT_CHANNELS;
      output[idx] = r;
      output[idx + 1] = g;
      output[idx + 2] = b;
    }
  }
}

// ==================== CLEANLINESS SCORE TO DISPENSE TIME ====================
unsigned int calculateDispenseTime(float cleanliness_score) {
  // Map cleanliness score (0-100) to dispense time (milliseconds)
  if (cleanliness_score < 30) {
    // Very dirty: 3 seconds
    return 3000;
  } else if (cleanliness_score < 60) {
    // Medium dirty: 2 seconds
    return 2000;
  } else if (cleanliness_score < 85) {
    // Lightly soiled: 1 second
    return 1000;
  } else {
    // Already clean: no dispense
    return 0;
  }
}

// ==================== SANITIZER CONTROL ====================
void dispenseSanitizer(unsigned int duration_ms) {
  if (duration_ms == 0) {
    Serial.println("Hands are clean - no sanitizer needed");
    return;
  }
  
  Serial.print("Dispensing sanitizer for ");
  Serial.print(duration_ms);
  Serial.println(" ms");
  
  // Turn on pump
  digitalWrite(PUMP_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);  // Visual feedback
  
  delay(duration_ms);
  
  // Turn off pump
  digitalWrite(PUMP_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("Dispensing complete");
}

// ==================== SETUP ====================
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n=== ESP32 Hand Sanitizer Dispenser ===");
  
  // Initialize GPIO
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  
  // Initialize camera
  if (!initCamera()) {
    Serial.println("Failed to initialize camera. Restarting...");
    delay(5000);
    ESP.restart();
  }
  
  // Initialize WiFi (optional)
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  int wifi_timeout = 0;
  while (WiFi.status() != WL_CONNECTED && wifi_timeout < 20) {
    delay(500);
    Serial.print(".");
    wifi_timeout++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi connection failed - continuing without WiFi");
  }
  
  Serial.println("\nSystem ready. Waiting for hand detection...");
  Serial.println("Place hand in front of camera to start detection.");
}

// ==================== MAIN LOOP ====================
void loop() {
  // Capture frame from camera
  camera_fb_t* fb = esp_camera_fb_get();
  
  if (!fb) {
    Serial.println("Camera capture failed");
    delay(1000);
    return;
  }
  
  Serial.println("\n--- Processing image ---");
  Serial.printf("Image size: %dx%d, format: %d\n", fb->width, fb->height, fb->format);
  
  // Preprocess image
  uint8_t processed_image[MODEL_INPUT_SIZE * MODEL_INPUT_SIZE * MODEL_INPUT_CHANNELS];
  preprocessImage(fb, processed_image);
  
  // Run inference (placeholder - replace with actual TFLite inference)
  float cleanliness_score = runInference(processed_image);
  
  // Calculate dispense time
  unsigned int dispense_time = calculateDispenseTime(cleanliness_score);
  
  // Display results
  Serial.printf("Cleanliness Score: %.2f/100\n", cleanliness_score);
  Serial.printf("Dispense Time: %d ms\n", dispense_time);
  
  // Dispense sanitizer
  dispenseSanitizer(dispense_time);
  
  // Return frame buffer
  esp_camera_fb_return(fb);
  
  // Wait before next detection
  delay(3000);  // 3 seconds between detections
}

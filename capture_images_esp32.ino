/*
 * ESP32-CAM Image Capture Script
 * Use this to capture images for your dataset
 * 
 * Instructions:
 * 1. Upload this sketch to ESP32-CAM
 * 2. Open Serial Monitor (115200 baud)
 * 3. Send commands via Serial Monitor:
 *    - 'c' or 'clean' - Capture clean hand image
 *    - 'm' or 'medium' - Capture medium cleanliness image
 *    - 'd' or 'dirty' - Capture dirty hand image
 *    - 's' - Show current count
 * 4. Images will be saved to SD card (if available) or sent via Serial
 * 
 * Alternative: Use ESP32-CAM web server to capture via browser
 */

#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>
#include <SD_MMC.h>

// ==================== CONFIGURATION ====================
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

WebServer server(80);

// Counters for each category
int clean_count = 0;
int medium_count = 0;
int dirty_count = 0;

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
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_VGA;  // 640x480 - good quality
  config.jpeg_quality = 12;  // 0-63, lower = higher quality
  config.fb_count = 1;
  
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return false;
  }
  return true;
}

void handleRoot() {
  String html = "<!DOCTYPE html><html><head>";
  html += "<meta name='viewport' content='width=device-width, initial-scale=1'>";
  html += "<style>body{font-family:Arial;text-align:center;background:#f0f0f0;}";
  html += "button{background:#4CAF50;color:white;padding:15px 32px;font-size:16px;";
  html += "border:none;border-radius:5px;margin:10px;cursor:pointer;}";
  html += "button:hover{background:#45a049;}";
  html += ".stats{background:white;padding:20px;margin:20px;border-radius:10px;display:inline-block;}";
  html += "</style></head><body>";
  html += "<h1>ESP32-CAM Dataset Capture</h1>";
  html += "<div class='stats'>";
  html += "<h2>Captured Images</h2>";
  html += "<p>Clean: " + String(clean_count) + "</p>";
  html += "<p>Medium: " + String(medium_count) + "</p>";
  html += "<p>Dirty: " + String(dirty_count) + "</p>";
  html += "</div><br>";
  html += "<button onclick='capture(\"clean\")'>Capture Clean Hand</button><br>";
  html += "<button onclick='capture(\"medium\")'>Capture Medium Hand</button><br>";
  html += "<button onclick='capture(\"dirty\")'>Capture Dirty Hand</button><br>";
  html += "<br><img id='preview' style='max-width:640px;border:2px solid #333;'><br>";
  html += "<script>";
  html += "function capture(category){";
  html += "document.getElementById('preview').src='/capture?cat='+category+'&t='+Date.now();";
  html += "fetch('/save?cat='+category).then(r=>r.text()).then(t=>alert(t));";
  html += "}";
  html += "</script></body></html>";
  server.send(200, "text/html", html);
}

void handleCapture() {
  String category = server.arg("cat");
  
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    server.send(500, "text/plain", "Camera capture failed");
    return;
  }
  
  server.send_P(200, "image/jpeg", (const char*)fb->buf, fb->len);
  esp_camera_fb_return(fb);
}

void handleSave() {
  String category = server.arg("cat");
  
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    server.send(500, "text/plain", "Camera capture failed");
    return;
  }
  
  // Increment counter
  if (category == "clean") clean_count++;
  else if (category == "medium") medium_count++;
  else if (category == "dirty") dirty_count++;
  
  // Try to save to SD card
  bool saved = false;
  if (SD_MMC.begin()) {
    String filename = "/" + category + "_" + String(millis()) + ".jpg";
    File file = SD_MMC.open(filename.c_str(), FILE_WRITE);
    if (file) {
      file.write(fb->buf, fb->len);
      file.close();
      saved = true;
      Serial.println("Saved to SD: " + filename);
    }
  }
  
  if (!saved) {
    // If no SD card, send via serial (you'll need to receive on PC)
    Serial.println("===IMAGE_START:" + category + "===");
    Serial.write(fb->buf, fb->len);
    Serial.println("===IMAGE_END===");
  }
  
  esp_camera_fb_return(fb);
  
  String response = "Saved " + category + " image #";
  if (category == "clean") response += String(clean_count);
  else if (category == "medium") response += String(medium_count);
  else if (category == "dirty") response += String(dirty_count);
  
  server.send(200, "text/plain", response);
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n=== ESP32-CAM Dataset Capture ===");
  
  // Initialize camera
  if (!initCamera()) {
    Serial.println("Camera init failed!");
    delay(5000);
    ESP.restart();
  }
  Serial.println("Camera initialized");
  
  // Initialize SD card (optional)
  if (SD_MMC.begin()) {
    Serial.println("SD card initialized");
  } else {
    Serial.println("SD card not found - images will be sent via Serial");
  }
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  int timeout = 0;
  while (WiFi.status() != WL_CONNECTED && timeout < 20) {
    delay(500);
    Serial.print(".");
    timeout++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.println("Open http://" + WiFi.localIP().toString() + " in your browser");
  } else {
    Serial.println("\nWiFi failed - use Serial commands instead");
  }
  
  // Setup web server
  server.on("/", handleRoot);
  server.on("/capture", handleCapture);
  server.on("/save", handleSave);
  server.begin();
  
  Serial.println("\n=== Ready ===");
  Serial.println("Commands via Serial:");
  Serial.println("  'c' or 'clean' - Capture clean hand");
  Serial.println("  'm' or 'medium' - Capture medium hand");
  Serial.println("  'd' or 'dirty' - Capture dirty hand");
  Serial.println("  's' - Show statistics");
}

void captureImage(String category) {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  
  // Increment counter
  if (category == "clean") clean_count++;
  else if (category == "medium") medium_count++;
  else if (category == "dirty") dirty_count++;
  
  // Try SD card first
  bool saved = false;
  if (SD_MMC.begin()) {
    String filename = "/" + category + "_" + String(millis()) + ".jpg";
    File file = SD_MMC.open(filename.c_str(), FILE_WRITE);
    if (file) {
      file.write(fb->buf, fb->len);
      file.close();
      saved = true;
      Serial.println("Saved: " + filename);
    }
  }
  
  if (!saved) {
    // Send via serial
    Serial.println("===IMAGE_START:" + category + "===");
    Serial.write(fb->buf, fb->len);
    Serial.println("===IMAGE_END===");
    Serial.println("Image sent via Serial - use receive script to save");
  }
  
  esp_camera_fb_return(fb);
  
  Serial.print(category + " images captured: ");
  if (category == "clean") Serial.println(clean_count);
  else if (category == "medium") Serial.println(medium_count);
  else if (category == "dirty") Serial.println(dirty_count);
}

void loop() {
  server.handleClient();
  
  // Handle serial commands
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toLowerCase();
    
    if (command == "c" || command == "clean") {
      captureImage("clean");
    } else if (command == "m" || command == "medium") {
      captureImage("medium");
    } else if (command == "d" || command == "dirty") {
      captureImage("dirty");
    } else if (command == "s" || command == "stats") {
      Serial.println("\n=== Statistics ===");
      Serial.println("Clean: " + String(clean_count));
      Serial.println("Medium: " + String(medium_count));
      Serial.println("Dirty: " + String(dirty_count));
      Serial.println("Total: " + String(clean_count + medium_count + dirty_count));
    }
  }
  
  delay(100);
}

"""
Simple HTTP server to upload images from phone via web browser
Run this on your computer, then open the IP address on your phone's browser
"""
import os
import http.server
import socketserver
from pathlib import Path
import urllib.parse
import shutil
from datetime import datetime

class ImageUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Upload Hand Images</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 600px;
                        margin: 50px auto;
                        padding: 20px;
                        background: #f5f5f5;
                    }
                    .container {
                        background: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }
                    h1 {
                        color: #333;
                        text-align: center;
                    }
                    .upload-area {
                        border: 3px dashed #4CAF50;
                        border-radius: 10px;
                        padding: 40px;
                        text-align: center;
                        margin: 20px 0;
                        background: #f9f9f9;
                    }
                    input[type="file"] {
                        display: none;
                    }
                    .file-label {
                        display: inline-block;
                        padding: 15px 30px;
                        background: #4CAF50;
                        color: white;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                    }
                    .file-label:hover {
                        background: #45a049;
                    }
                    button {
                        padding: 15px 30px;
                        background: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 16px;
                        cursor: pointer;
                        margin-top: 20px;
                        width: 100%;
                    }
                    button:hover {
                        background: #0b7dda;
                    }
                    select {
                        padding: 10px;
                        font-size: 16px;
                        width: 100%;
                        margin: 10px 0;
                        border-radius: 5px;
                        border: 1px solid #ddd;
                    }
                    #fileList {
                        margin-top: 20px;
                        text-align: left;
                    }
                    .file-item {
                        padding: 10px;
                        background: #f0f0f0;
                        margin: 5px 0;
                        border-radius: 5px;
                    }
                    .status {
                        margin-top: 20px;
                        padding: 15px;
                        border-radius: 5px;
                        display: none;
                    }
                    .success {
                        background: #d4edda;
                        color: #155724;
                        border: 1px solid #c3e6cb;
                    }
                    .error {
                        background: #f8d7da;
                        color: #721c24;
                        border: 1px solid #f5c6cb;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📸 Upload Hand Images</h1>
                    <p style="text-align: center; color: #666;">
                        Select images from your phone and choose category
                    </p>
                    
                    <div class="upload-area">
                        <label for="fileInput" class="file-label">
                            📁 Choose Images
                        </label>
                        <input type="file" id="fileInput" multiple accept="image/*">
                        <p id="fileCount" style="margin-top: 15px; color: #666;"></p>
                    </div>
                    
                    <select id="category">
                        <option value="clean">Clean Hands</option>
                        <option value="medium">Medium Cleanliness</option>
                        <option value="dirty">Dirty Hands</option>
                    </select>
                    
                    <div id="fileList"></div>
                    
                    <button onclick="uploadFiles()">Upload Images</button>
                    
                    <div id="status" class="status"></div>
                </div>
                
                <script>
                    const fileInput = document.getElementById('fileInput');
                    const fileList = document.getElementById('fileList');
                    const fileCount = document.getElementById('fileCount');
                    const categorySelect = document.getElementById('category');
                    
                    fileInput.addEventListener('change', function(e) {
                        const files = e.target.files;
                        fileCount.textContent = files.length + ' file(s) selected';
                        
                        fileList.innerHTML = '';
                        for (let i = 0; i < files.length; i++) {
                            const div = document.createElement('div');
                            div.className = 'file-item';
                            div.textContent = (i+1) + '. ' + files[i].name;
                            fileList.appendChild(div);
                        }
                    });
                    
                    function uploadFiles() {
                        const files = fileInput.files;
                        const category = categorySelect.value;
                        
                        if (files.length === 0) {
                            showStatus('Please select at least one image', 'error');
                            return;
                        }
                        
                        const formData = new FormData();
                        formData.append('category', category);
                        
                        for (let i = 0; i < files.length; i++) {
                            formData.append('files', files[i]);
                        }
                        
                        showStatus('Uploading...', 'success');
                        
                        fetch('/upload', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.text())
                        .then(data => {
                            showStatus('Success! ' + data, 'success');
                            fileInput.value = '';
                            fileList.innerHTML = '';
                            fileCount.textContent = '';
                        })
                        .catch(error => {
                            showStatus('Error: ' + error, 'error');
                        });
                    }
                    
                    function showStatus(message, type) {
                        const status = document.getElementById('status');
                        status.textContent = message;
                        status.className = 'status ' + type;
                        status.style.display = 'block';
                    }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/upload':
            try:
                content_type = self.headers['Content-Type']
                if not content_type.startswith('multipart/form-data'):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid content type')
                    return
                
                # Parse multipart form data
                form_data = self.rfile.read(int(self.headers['Content-Length']))
                
                # Extract category and files
                boundary = content_type.split('boundary=')[1]
                parts = form_data.split(b'--' + boundary.encode())
                
                category = None
                files_data = []
                
                for part in parts:
                    if b'name="category"' in part:
                        # Extract category value
                        lines = part.split(b'\r\n')
                        for line in lines:
                            if b'category' in line and b'name=' in line:
                                continue
                            if line and not line.startswith(b'Content-'):
                                category = line.decode('utf-8').strip()
                                break
                    elif b'name="files"' in part and b'filename=' in part:
                        # Extract file
                        header_end = part.find(b'\r\n\r\n')
                        if header_end != -1:
                            file_data = part[header_end + 4:]
                            # Remove trailing boundary
                            if file_data.endswith(b'\r\n'):
                                file_data = file_data[:-2]
                            files_data.append(file_data)
                
                if not category or not files_data:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Missing category or files')
                    return
                
                # Save files
                saved_count = 0
                target_dir = Path('raw_data') / category
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Get current count
                existing_files = list(target_dir.glob('*.jpg')) + list(target_dir.glob('*.png'))
                start_num = len(existing_files) + 1
                
                for i, file_data in enumerate(files_data):
                    if len(file_data) < 100:  # Skip empty parts
                        continue
                    
                    # Determine extension (assume jpg)
                    ext = '.jpg'
                    if file_data[:4] == b'\x89PNG':
                        ext = '.png'
                    
                    filename = f"{category}_{start_num + i:04d}{ext}"
                    file_path = target_dir / filename
                    
                    with open(file_path, 'wb') as f:
                        f.write(file_data)
                    
                    saved_count += 1
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Uploaded {saved_count} image(s) to {category} folder'.encode())
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Error: {str(e)}'.encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_server(port=8000):
    """Start the upload server"""
    # Create raw_data directories
    for category in ['clean', 'medium', 'dirty']:
        Path(f'raw_data/{category}').mkdir(parents=True, exist_ok=True)
    
    handler = ImageUploadHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # Try to get actual local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            pass
        
        print("="*60)
        print("Phone Image Upload Server")
        print("="*60)
        print(f"\nServer running on:")
        print(f"  Local: http://localhost:{port}")
        print(f"  Network: http://{local_ip}:{port}")
        print(f"\nOn your phone:")
        print(f"  1. Connect to same WiFi network")
        print(f"  2. Open browser")
        print(f"  3. Go to: http://{local_ip}:{port}")
        print(f"  4. Upload images and select category")
        print(f"\nPress Ctrl+C to stop")
        print("="*60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Start web server for phone image upload')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port number (default: 8000)')
    
    args = parser.parse_args()
    
    start_server(args.port)

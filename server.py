#!/usr/bin/env python3
import http.server
import socketserver
import socket
import qrcode
from io import BytesIO
import base64

PORT = 8000

def get_local_ip():
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/qr':
            local_ip = get_local_ip()
            url = f"http://{local_ip}:{PORT}/audiotour.html"
            qr_data = generate_qr_code(url)
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>QR Code Scanner</title>
                <style>
                    body {{ font-family: Arial; text-align: center; padding: 20px; }}
                    .qr-container {{ margin: 20px; }}
                    img {{ max-width: 300px; }}
                </style>
            </head>
            <body>
                <h1>Scan deze QR code met je Samsung S21</h1>
                <div class="qr-container">
                    <img src="data:image/png;base64,{qr_data}" alt="QR Code">
                </div>
                <p><strong>Of ga naar:</strong><br><a href="{url}">{url}</a></p>
                <p>Zorg ervoor dat je telefoon op hetzelfde WiFi netwerk zit!</p>
            </body>
            </html>
            """
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    local_ip = get_local_ip()
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Server draait op http://{local_ip}:{PORT}")
        print(f"QR Code: http://{local_ip}:{PORT}/qr")
        print(f"Audio Tour: http://{local_ip}:{PORT}/audiotour.html")
        print("\nDruk Ctrl+C om te stoppen")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer gestopt")
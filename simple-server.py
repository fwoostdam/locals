#!/usr/bin/env python3
import http.server
import socketserver
import socket

PORT = 8000

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == "__main__":
    local_ip = get_local_ip()
    
    with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"🌐 Server draait op: http://{local_ip}:{PORT}")
        print(f"📱 Audio Tour: http://{local_ip}:{PORT}/audiotour.html")
        print(f"🎯 Scoreboard: http://{local_ip}:{PORT}/scoreboard.html")
        print(f"🎰 Slotmachine: http://{local_ip}:{PORT}/slotmachine.html")
        print(f"\n📋 Stappen voor je Samsung S21:")
        print(f"1. Zorg dat je telefoon op hetzelfde WiFi zit")
        print(f"2. Open browser op telefoon")
        print(f"3. Ga naar: http://{local_ip}:{PORT}/audiotour.html")
        print(f"4. Geef toestemming voor locatie toegang")
        print(f"\n⏹️  Druk Ctrl+C om te stoppen")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server gestopt")
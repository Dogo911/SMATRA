import socket

def try_ip(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((ip, 10940))
        s.sendall(b"\n")
        data = s.recv(1024)
        if b"SCIP" in data:
            print(f"✅ Hokuyo gefunden bei {ip}")
        s.close()
    except Exception:
        pass

# IP-Range: 192.168.0.1 bis 192.168.0.254
for i in range(1, 255):
    ip = f"192.168.0.{i}"
    try_ip(ip)

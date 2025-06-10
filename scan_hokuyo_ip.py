import socket

def test_ip(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        sock.connect((ip, 10940))
        print(f"✅ Gerät gefunden auf {ip}")
    except:
        pass
    finally:
        sock.close()

for i in range(1, 255):
    ip = f"192.168.0.{i}"
    test_ip(ip)

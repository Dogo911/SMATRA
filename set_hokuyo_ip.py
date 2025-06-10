import socket

target_ip = "192.168.0.1"  # Jetson-IP (aktuell)
target_port = 10940

# Neue IP, die wir setzen wollen
new_ip = "192.168.0.10"
new_ip_cmd = f"IP{new_ip.replace('.', '')}\n"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)

try:
    sock.connect((target_ip, target_port))
    print("✅ Verbunden! Sende Befehl zum Setzen der neuen IP...")
    sock.sendall(new_ip_cmd.encode())
    response = sock.recv(1024)
    print(f"Antwort: {response}")
    sock.close()
except Exception as e:
    print(f"❌ Fehler: {e}")

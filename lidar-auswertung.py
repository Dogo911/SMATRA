import socket
import time
import string

LIDAR_IP = "192.168.0.10"
LIDAR_PORT = 10940

def send_command(sock, cmd):
    sock.sendall((cmd + '\r').encode())

def receive_response(sock, timeout=2.0):
    sock.settimeout(timeout)
    data = b""
    try:
        while True:
            part = sock.recv(4096)
            if not part:
                break
            data += part
            if b"\n\n" in data or b"\r\n\r\n" in data:
                break
    except socket.timeout:
        pass
    return data.decode(errors='replace')

def extract_distances(response):
    lines = response.splitlines()
    data_lines = []
    header_skipped = 0
    for line in lines:
        if header_skipped < 2:
            header_skipped += 1
            continue
        if line == '':
            break
        if line[0] not in string.ascii_letters + string.digits:
            continue
        if len(line) > 1:
            data_lines.append(line[:-1])
    data_str = ''.join(data_lines)
    data_str = data_str[3:]
    distances = []
    for i in range(0, len(data_str), 3):
        chunk = data_str[i:i+3]
        if len(chunk) != 3:
            continue
        val = ((ord(chunk[0]) - 0x30) << 12) | ((ord(chunk[1]) - 0x30) << 6) | (ord(chunk[2]) - 0x30)
        distances.append(val)
    return distances[:1081]
    
def print_distances(distances, count_per_line=20):
    formatted = [
        f"{d:.3f}" if d is not None and d < 100 else "---"
        for d in distances
    ]
    for i in range(0, len(formatted), count_per_line):
        print(" | ".join(formatted[i:i+count_per_line]))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((LIDAR_IP, LIDAR_PORT))
    print("Verbunden mit UST-10LX.")

    send_command(s, "BM")
    time.sleep(0.1)
    response = receive_response(s)
    print("BM-Antwort:", response)

    try:
        while True:
            send_command(s, "GD0000108000")
            time.sleep(0.05)
            response = receive_response(s)
            distances = extract_distances(response)
            distances_m = [round(d / 1000, 3) for d in distances]
            print_distances(distances_m)
            print('-' * 120)
    except KeyboardInterrupt:
        print("Beende Messung...")
    finally:
        send_command(s, "QT")
        print("LiDAR gestoppt.")


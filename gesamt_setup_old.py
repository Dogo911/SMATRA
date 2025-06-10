import subprocess
import time

print("🚀 Starte Startup-Skript...")
startup_proc = subprocess.Popen(["python3", "/home/ubuntu/startup_5.1.py"])
startup_proc.wait()

print("🔧 Setze DNS (nameserver 8.8.8.8)...")
dns_fix_cmd = 'echo "smatra1234" | sudo -S bash -c \'echo "nameserver 8.8.8.8" > /etc/resolv.conf\''
subprocess.run(dns_fix_cmd, shell=True)

print("⏳ Warte 3 Sekunden...")
time.sleep(3)

print("🚀 Starte RAPI-Inbetriebnahme...")
rapi_proc = subprocess.Popen(["python3", "/home/smarttraversejetson/rapi_ibn2.py"])

print("⏳ Warte 3 Sekunden nach RAPI...")
time.sleep(3)

print("🚀 Starte LIDAR Setup...")
lidar_proc = subprocess.Popen(["bash", "/home/smarttraversejetson/setup_lidar_ibn.sh"])

print("⏳ Warte 5 Sekunden nach LiDAR...")
time.sleep(5)

print("🚀 Starte Detection...")
det_proc = subprocess.Popen(["bash", "/home/smarttraversejetson/start_det.sh"])

rapi_proc.wait()
lidar_proc.wait()
det_proc.wait()

print("✅ Gesamt-Setup abgeschlossen.")


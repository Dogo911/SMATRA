import subprocess
import os

def run_command(command, use_sudo=False, password=None, shell=False):
    if use_sudo and password:
        command = f'echo {password} | sudo -S {command}'
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True, env=os.environ)

def route_exists(ip):
    result = subprocess.run(f"ip route | grep '^{ip} '", shell=True, stdout=subprocess.PIPE)
    return result.returncode == 0

def main():
    password = "smatra1234"

    try:
        print("\n🔧 Initialisiere ROS2 Umgebung ...")
        ros_setup_cmd = "source /opt/ros/humble/setup.bash && env"
        proc = subprocess.Popen(ros_setup_cmd, stdout=subprocess.PIPE, shell=True, executable="/bin/bash")
        output, _ = proc.communicate()
        env_vars = dict(line.split("=", 1) for line in output.decode().splitlines() if "=" in line)
        os.environ.update(env_vars)
        os.environ["ROS_DOMAIN_ID"] = "5"
        print("✅ ROS2 Umgebung gesetzt. ROS_DOMAIN_ID=5")

        # Ethernet-Interface & Lidar-Konfiguration
        lidar_interface = "enP8p1s0"  # statt "enP8p1s0"  "enx606d3ccc5c04"
        lidar_ip = "192.168.0.10"
        lidar_mac = "00:1d:9b:1e:0e:02"

        print(f"\n📍 Trage statisch ARP für Lidar {lidar_ip} ({lidar_mac}) auf {lidar_interface} ein ...")
        run_command(f"arp -s {lidar_ip} {lidar_mac} -i {lidar_interface}", use_sudo=True, password=password)

        if not route_exists(lidar_ip):
            print(f"📍 Setze Route für {lidar_ip} über {lidar_interface} ...")
            run_command(f"ip route add {lidar_ip} dev {lidar_interface}", use_sudo=True, password=password)
        else:
            print(f"ℹ️  Route zu {lidar_ip} besteht bereits – kein Eintrag nötig.")

        print(f"\n🚀 Starte ROS2 Lidar-Node auf Ziel-IP {lidar_ip} ...")
        run_command(
            f"ros2 run urg_node urg_node_driver --ros-args -p ip_address:={lidar_ip}",
            shell=True
        )

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Fehler beim Ausführen eines Befehls: {e}")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main()


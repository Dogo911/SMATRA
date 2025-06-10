import subprocess
import os

def run_command(command, use_sudo=False, password=None, shell=False):
    if use_sudo and password:
        command = f'echo {password} | sudo -S {command}'
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True, env=os.environ)

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

        # Ethernet-Interface konfigurieren
        lidar_interface = "enP8p1s0"
        lidar_jetson_ip = "192.168.0.200"
        lidar_target_ip = "192.168.0.10"

        print(f"\n🌐 Setze Jetson-IP auf {lidar_jetson_ip} für Interface {lidar_interface} ...")
        run_command(f"ip addr add {lidar_jetson_ip}/24 dev {lidar_interface}", use_sudo=True, password=password)

        print(f"📍 Setze statische Route zu {lidar_target_ip} über {lidar_interface} ...")
        run_command(f"ip route add {lidar_target_ip} dev {lidar_interface}", use_sudo=True, password=password)

        # Lidar-Node starten
        print(f"\n🚀 Starte ROS2 Lidar-Node auf Ziel-IP {lidar_target_ip} ...")
        run_command(
            f"ros2 run urg_node urg_node_driver --ros-args -p ip_address:={lidar_target_ip}",
            shell=True
        )

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Fehler beim Ausführen eines Befehls: {e}")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main()


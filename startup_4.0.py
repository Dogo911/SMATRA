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
        # 1. (optional) DNS setzen – nur nötig bei DNS-Problemen
        # run_command('echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf', use_sudo=True, password=password)

        # 2. ROS2 vorbereiten
        ros_setup_cmd = "source /opt/ros/humble/setup.bash && env"
        proc = subprocess.Popen(ros_setup_cmd, stdout=subprocess.PIPE, shell=True, executable="/bin/bash")
        output, _ = proc.communicate()
        env_vars = dict(line.split("=", 1) for line in output.decode().splitlines() if "=" in line)

        os.environ.update(env_vars)

        # ROS Domain setzen
        os.environ["ROS_DOMAIN_ID"] = "5"

        # 3. Ethernet-Interface für Lidar konfigurieren
        lidar_interface = "enP8p1s0"
        lidar_ip = "192.168.10.1"
        lidar_target_ip = "192.168.10.10"

        run_command(f"ip addr flush dev {lidar_interface}", use_sudo=True, password=password)
        run_command(f"ip addr add {lidar_ip}/24 dev {lidar_interface}", use_sudo=True, password=password)

        # 4. Lidar Node starten (ROS2)
        run_command(
            f"ros2 run urg_node urg_node_driver --ros-args -p ip_address:={lidar_target_ip}",
            shell=True
        )

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


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
        # 1. Set DNS resolver
        run_command('echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf', use_sudo=True, password=password)

        # 2. Source ROS setup and export environment variables
        ros_setup_cmd = "source /opt/ros/humble/setup.bash && env"
        proc = subprocess.Popen(ros_setup_cmd, stdout=subprocess.PIPE, shell=True, executable="/bin/bash")
        output, _ = proc.communicate()
        env_vars = dict(line.split("=", 1) for line in output.decode().splitlines() if "=" in line)
        os.environ.update(env_vars)

        # Set ROS_DOMAIN_ID
        os.environ["ROS_DOMAIN_ID"] = "5"

        # 3. Clean and set LAN IP
        try:
            run_command("ip addr del 192.168.0.10/24 dev enP8p1s0", use_sudo=True, password=password)
        except subprocess.CalledProcessError:
            print("IP 192.168.0.10 was not set on enP8p1s0 – skipping delete.")

        run_command("ip addr add 192.168.0.100/24 dev enP8p1s0", use_sudo=True, password=password)
        run_command("ip route add 192.168.0.10 dev enP8p1s0", use_sudo=True, password=password)

        # 4. Start ROS2 node for the LiDAR
        run_command(
            "ros2 run urg_node urg_node_driver --ros-args -p ip_address:=192.168.0.10",
            shell=True,
            use_sudo=False,
            password=None,
        )

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


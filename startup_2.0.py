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

        # 2. Source ROS setup and export env
        ros_setup_cmd = "source /opt/ros/humble/setup.bash && env"
        proc = subprocess.Popen(ros_setup_cmd, stdout=subprocess.PIPE, shell=True, executable="/bin/bash")
        output, _ = proc.communicate()
        env_vars = dict(line.split("=", 1) for line in output.decode().splitlines() if "=" in line)

        os.environ.update(env_vars)

        # --> Hier ROS_DOMAIN_ID setzen
        os.environ["ROS_DOMAIN_ID"] = "5"

        # 3. Flush and set IP address
        run_command("ip addr flush dev enP8p1s0", use_sudo=True, password=password)
        run_command("ip addr add 192.168.0.1/24 dev enP8p1s0", use_sudo=True, password=password)

        # 4. Start ROS2 node in Domain 5
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


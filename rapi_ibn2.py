#import os
#import sys
#import subprocess

#def already_running():
#    result = subprocess.run(['pgrep', '-f', os.path.basename(__file__)], stdout=subprocess.PIPE)
#    pids = result.stdout.decode().strip().split('\n')
#    return len([p for p in pids if p and int(p) != os.getpid()]) > 0

#if already_running():
#    print("⚠️ Dieses Script läuft bereits – beende mich.")
#    sys.exit(0)




import paramiko
import threading
import time

HOST = "192.168.0.60"
USERNAME = "ubuntu"
PASSWORD = "traverse1234"

ROS_SETUP = "source /opt/ros/noetic/setup.bash"
CATKIN_SETUP = "source ~/catkin_ws/devel/setup.bash"

def start_terminal(name, commands, delay=0):
    def run():
        print(f"[{name}] Starte nach {delay}s...")
        time.sleep(delay)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOST, username=USERNAME, password=PASSWORD)

        for cmd in commands:
            print(f"[{name}] → {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            if "sudo" in cmd:
                stdin.write(PASSWORD + "\n")
                stdin.flush()
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(f"[{name}] Ausgabe: {output.strip()}")
            if error:
                print(f"[{name}] Fehler: {error.strip()}")
            time.sleep(1)

        print(f"[{name}] Fertig.")
    thread = threading.Thread(target=run)
    thread.start()
    return thread

if __name__ == "__main__":
    t1 = start_terminal("Terminal 1", [
        f"{ROS_SETUP} && {CATKIN_SETUP} && roscore"
    ], delay=0)

    t2 = start_terminal("Terminal 2", [
        f"{ROS_SETUP} && {CATKIN_SETUP} && python3 ~/rest_listener.py"
    ], delay=5)

    t3 = start_terminal("Terminal 3", [
        f"{ROS_SETUP} && {CATKIN_SETUP} && sudo python3 ~/catkin_ws/src/test/scripts/travio.py"
    ], delay=10)

    t1.join()
    t2.join()
    t3.join()


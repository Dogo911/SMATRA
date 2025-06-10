#!/bin/bash

# Setze DISPLAY für GUI
export DISPLAY=:0

# Zugangsdaten
USER="ubuntu"
HOST="192.168.0.60"
PASS="traverse1234"

# Terminal 4: SSH zum Raspberry Pi und roscore starten
gnome-terminal -- bash -c "sshpass -p '$PASS' ssh $USER@$HOST 'cd ~/catkin_ws && source ./devel/setup.bash && roscore'; exec bash"

sleep 5

# Terminal 5: SSH zum Raspberry Pi und rest_listener starten
gnome-terminal -- bash -c "sshpass -p '$PASS' ssh $USER@$HOST 'python3 rest_listener.py'; exec bash"

sleep 3

# Terminal 6: SSH zum Raspberry Pi und travio.py (mit sudo) starten
gnome-terminal -- bash -c "sshpass -p '$PASS' ssh $USER@$HOST 'echo $PASS | sudo -S python3 ~/catkin_ws/src/test/scripts/travio.py'; exec bash"

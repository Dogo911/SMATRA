#!/bin/bash

export DISPLAY=:0

source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=5

# Terminal 1: Startup
gnome-terminal -- bash -c "python3 /home/smarttraversejetson/startup_5.1.py; exec bash"

# Terminal 2: ROS-Umgebung und /scan anzeigen
gnome-terminal -- bash -c "source /opt/ros/humble/setup.bash && export ROS_DOMAIN_ID=5 && ros2 topic echo /scan; exec bash"

# Terminal 3: ROS Workspace bauen und Node starten
gnome-terminal -- bash -c 'cd ~/ros2_ws && colcon build && source install/setup.bash && export ROS_DOMAIN_ID=5 && ros2 run lidar_speed truck_speed_monitor_modified_2; exec bash'


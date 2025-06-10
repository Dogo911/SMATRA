import rclpy
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions, StorageFilter
import matplotlib.pyplot as plt
import os

# === Pfad zur Bag-Datei ===
bag_path = "/home/smarttraversejetson/bags/truck_speed_test/rosbag2_2025_06_04-16_42_19"

# === Pfad zur Datei mit den LiDAR-Messungen ===
lidar_file = "/home/smarttraversejetson/bags/lidar_speeds.txt"

# === Topic und Typ ===
topic_name = "/truck_state"
msg_type_str = "truck_msgs/msg/ZfTruckState"

# === ROS2-Bag vorbereiten ===
rclpy.init()
reader = SequentialReader()
storage_options = StorageOptions(uri=bag_path, storage_id='sqlite3')
converter_options = ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
reader.open(storage_options, converter_options)
reader.set_filter(StorageFilter(topics=[topic_name]))
msg_type = get_message(msg_type_str)

# === TruckState-Daten auslesen ===
timestamps = []
truck_speeds_kmh = []

while reader.has_next():
    topic, data, t = reader.read_next()
    msg = deserialize_message(data, msg_type)
    speed_kmh = msg.v / 1000 * 3.6
    timestamps.append(t * 1e-9)
    truck_speeds_kmh.append(speed_kmh)

# === LiDAR-Werte einlesen ===
lidar_speeds = []
if os.path.exists(lidar_file):
    with open(lidar_file, "r") as f:
        for line in f:
            try:
                speed = float(line.strip())
                lidar_speeds.append(speed)
            except:
                continue

# === Zeitfenster aufteilen für LiDAR-Werte ===
t_start = timestamps[0]
t_end = timestamps[-1]
total_duration = t_end - t_start

if len(lidar_speeds) == 0:
    print("⚠️ Keine LiDAR-Werte gefunden.")
    lidar_speeds = []

lidar_times = []
if lidar_speeds:
    segment = total_duration / len(lidar_speeds)
    for i in range(len(lidar_speeds)):
        center = t_start + segment * (i + 0.5)
        lidar_times.append(center)

# === Plot erstellen ===
plt.figure()
plt.plot(timestamps, truck_speeds_kmh, label="Truck-Geschwindigkeit [km/h]", alpha=0.7)

avg_truck = sum(truck_speeds_kmh)/len(truck_speeds_kmh)
plt.hlines(y=avg_truck, xmin=t_start, xmax=t_end, colors='r', linestyle='--', label='Truck Ø-Geschwindigkeit')

# LiDAR-Werte einzeichnen
for t, v in zip(lidar_times, lidar_speeds):
    plt.hlines(y=v, xmin=t - segment/2, xmax=t + segment/2, colors='g', linewidth=2)

if lidar_speeds:
    avg_lidar = sum(lidar_speeds)/len(lidar_speeds)
    plt.hlines(y=avg_lidar, xmin=t_start, xmax=t_end, colors='green', linestyle='--', label='LiDAR Ø-Geschwindigkeit')

plt.title("Mehrfache Durchfahrten: TruckState vs. LiDAR")
plt.xlabel("Zeit [s]")
plt.ylabel("Geschwindigkeit [km/h]")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

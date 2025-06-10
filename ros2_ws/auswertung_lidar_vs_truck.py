import rclpy
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions, StorageFilter
import math
import matplotlib.pyplot as plt

# === ANPASSEN: Pfad zur Bag-Datei ===
bag_path = "/home/smarttraversejetson/bags/vergleich_lidar_truck/rosbag2_2025_06_04-18_41_51"

# === Topics und Nachrichtentypen ===
topic_scan = "/scan"
topic_truck = "/truck_state"
msg_type_scan = "sensor_msgs/msg/LaserScan"
msg_type_truck = "truck_msgs/msg/ZfTruckState"

# === LiDAR-Kalibrier- und Messparameter ===
beta_deg = 8.0
trigger_threshold = 0.03
min_calibration_scans = 5

# === ROS2-Bag initialisieren ===
rclpy.init()
reader = SequentialReader()
storage_options = StorageOptions(uri=bag_path, storage_id='sqlite3')
converter_options = ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
reader.open(storage_options, converter_options)
reader.set_filter(StorageFilter(topics=[topic_scan, topic_truck]))

scan_type = get_message(msg_type_scan)
truck_type = get_message(msg_type_truck)

# === Daten speichern ===
truck_times = []
truck_speeds = []
scan_timestamps = []
scan_ranges = []

# === Lesen der Bag ===
while reader.has_next():
    topic, data, t = reader.read_next()
    if topic == topic_truck:
        msg = deserialize_message(data, truck_type)
        v_kmh = msg.v / 1000 * 3.6
        truck_times.append(t * 1e-9)
        truck_speeds.append(v_kmh)
    elif topic == topic_scan:
        msg = deserialize_message(data, scan_type)
        scan_timestamps.append(msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9)
        scan_ranges.append(list(msg.ranges))
        if 'angle_min' not in locals():
            angle_min = msg.angle_min
            angle_increment = msg.angle_increment

# === Kalibrierung (wie in deinem Node)
beta_rad = math.radians(beta_deg)
neg_index = int(round((-beta_rad - angle_min) / angle_increment))
pos_index = int(round(( beta_rad - angle_min) / angle_increment))

mean_zero = sum(scan[neg_index] for scan in scan_ranges[:min_calibration_scans]) / min_calibration_scans
mean_min  = sum(min(scan[neg_index], scan[pos_index]) for scan in scan_ranges[:min_calibration_scans]) / min_calibration_scans
h = mean_min

sigma = math.acos(h / mean_zero)
x = math.tan(sigma + beta_rad) * h
y = math.tan(sigma - beta_rad) * h
d = x - y  # gemessene Strecke in Metern

# === Durchfahrten erkennen & LiDAR-Geschwindigkeiten berechnen
ref_neg = scan_ranges[0][neg_index]
ref_pos = scan_ranges[0][pos_index]
state = "waiting"
start_time = None
lidar_speeds = []

for i, scan in enumerate(scan_ranges):
    t = scan_timestamps[i]
    r_neg = scan[neg_index]
    r_pos = scan[pos_index]

    if state == "waiting" and (ref_neg - r_neg) > trigger_threshold:
        start_time = t
        state = "running"
    elif state == "running" and (ref_pos - r_pos) > trigger_threshold:
        dt = t - start_time
        if dt > 0:
            v_mps = d / dt
            v_kmh = v_mps * 3.6
            lidar_speeds.append((start_time + dt / 2, v_kmh))
        state = "clearing"
    elif state == "clearing" and (r_pos - ref_pos) > -trigger_threshold:
        state = "waiting"

# === Plot
plt.figure()
plt.plot(truck_times, truck_speeds, label="TruckState Geschwindigkeit [km/h]", alpha=0.7)

# LiDAR Einzelwerte
for t, v in lidar_speeds:
    plt.hlines(y=v, xmin=t - 0.5, xmax=t + 0.5, colors="green", linewidth=2, label="LiDAR Messung" if "LiDAR Messung" not in plt.gca().get_legend_handles_labels()[1] else "")

# Durchschnitte
if truck_speeds:
    plt.hlines(y=sum(truck_speeds)/len(truck_speeds), xmin=min(truck_times), xmax=max(truck_times), colors='r', linestyle='--', label='Truck Ø')
if lidar_speeds:
    avg_lidar = sum(v for _, v in lidar_speeds) / len(lidar_speeds)
    plt.hlines(y=avg_lidar, xmin=min(truck_times), xmax=max(truck_times), colors='green', linestyle='--', label='LiDAR Ø')

plt.xlabel("Zeit [s]")
plt.ylabel("Geschwindigkeit [km/h]")
plt.title("Vergleich LiDAR vs. Truck Geschwindigkeit")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

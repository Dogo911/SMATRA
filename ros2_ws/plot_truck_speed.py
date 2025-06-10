import rclpy
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions, StorageFilter
import matplotlib.pyplot as plt

# === Pfad zur Bag-Datei anpassen ===
bag_path = "/home/smarttraversejetson/bags/truck_speed_test/rosbag2_2025_06_04-16_42_19"

# === Topic und Nachrichtentyp ===
topic_name = "/truck_state"
msg_type_str = "truck_msgs/msg/ZfTruckState"

# === ROS2-Bag öffnen ===
rclpy.init()
reader = SequentialReader()
storage_options = StorageOptions(uri=bag_path, storage_id='sqlite3')
converter_options = ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
reader.open(storage_options, converter_options)

# === Nur gewünschtes Topic filtern ===
reader.set_filter(StorageFilter(topics=[topic_name]))

# === Nachrichtentyp laden ===
msg_type = get_message(msg_type_str)

# === Daten extrahieren ===
timestamps = []
speeds_kmh = []

while reader.has_next():
    topic, data, t = reader.read_next()
    msg = deserialize_message(data, msg_type)
    speed_kmh = msg.v / 1000 * 3.6  # mm/s → km/h
    timestamps.append(t * 1e-9)      # ns → s
    speeds_kmh.append(speed_kmh)

# === Plot erstellen ===
plt.figure()
plt.plot(timestamps, speeds_kmh, marker='o', label="Truck-Geschwindigkeit [km/h]")
plt.hlines(y=sum(speeds_kmh)/len(speeds_kmh), xmin=timestamps[0], xmax=timestamps[-1],
           colors='r', linestyle='--', label='Durchschnitt')

plt.title("Truck-Geschwindigkeit aus /truck_state")
plt.xlabel("Zeit [s]")
plt.ylabel("Geschwindigkeit [km/h]")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()


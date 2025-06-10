import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import time
import math

class SpeedDetector(Node):
    def __init__(self):
        super().__init__('speed_detector')

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)

        self.start_time = None
        self.measurement_started = False
        self.object_detected = False  # Neu: Status, ob aktuell ein Objekt erkannt wird

        self.start_threshold = 0.6  # Start bei 0.6m
        self.stop_threshold = 0.5   # Stop bei 0.5m
        self.detect_angle_min = -2  # links in Grad
        self.detect_angle_max = 2   # rechts in Grad
        self.lidar_angle_deg = 47   # winkel in dem lidar auf fahrzeug trifft 
        self.lidar_angle_rad = math.radians(self.lidar_angle_deg) # umrechnung winkel in rad

    def scan_callback(self, msg):
        num_points = len(msg.ranges)
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment

        index_min = int((self.detect_angle_min * 3.1415/180.0 - angle_min) / angle_increment)
        index_max = int((self.detect_angle_max * 3.1415/180.0 - angle_min) / angle_increment)

        index_min = max(0, min(num_points-1, index_min))
        index_max = max(0, min(num_points-1, index_max))

        region = msg.ranges[index_min:index_max]

        min_distance = min(region)  # Wichtig: nur auf die nächste Entfernung reagieren

        if not self.measurement_started:
            # Startbedingung: Abstand kleiner als 0.6m, aber größer als 0.5m
            if self.stop_threshold < min_distance <= self.start_threshold and not self.object_detected:
                self.start_time = time.time()
                self.measurement_started = True
                self.object_detected = True  # Objekt erkannt
                self.get_logger().info("0.6m Grenze durchstoßen - Zeitmessung gestartet.")

        else:
            # Stoppbedingung: Abstand kleiner als 0.5m
            if min_distance <= self.stop_threshold:
                end_time = time.time()
                duration = end_time - self.start_time
                self.measurement_started = False

                # Strecke zwischen 0.6m und 0.5m (0.1m)
                Strecke_in_Meter = (self.start_threshold - self.stop_threshold) / math.cos(self.lidar_angle_rad)
                Geschwindigkeit = Strecke_in_Meter / duration  # m/s
                Geschwindigkeit_kmh = Geschwindigkeit * 3.6    # in km/h

                self.get_logger().info(f"Geschwindigkeit: {Geschwindigkeit_kmh:.2f} km/h (Zeit: {duration:.3f} s)")

        # Reset-Logik: Objekt ist weg (Entfernung wieder > 0.6m)
        if min_distance > self.start_threshold:
            self.object_detected = False

# >>>>>> HIER fehlt bei dir bisher alles! <<<<<<
def main(args=None):
    rclpy.init(args=args)
    node = SpeedDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


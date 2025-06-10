import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import time

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
        self.start_threshold = 0.6  # Start bei 0.6m
        self.stop_threshold = 0.5   # Stop bei 0.5m
        self.detect_angle_min = -15  # links in Grad
        self.detect_angle_max = 15   # rechts in Grad

    def scan_callback(self, msg):
        num_points = len(msg.ranges)
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment

        index_min = int((self.detect_angle_min * 3.1415/180.0 - angle_min) / angle_increment)
        index_max = int((self.detect_angle_max * 3.1415/180.0 - angle_min) / angle_increment)

        index_min = max(0, min(num_points-1, index_min))
        index_max = max(0, min(num_points-1, index_max))

        region = msg.ranges[index_min:index_max]

        for distance in region:
            # Startbedingung: Unterschreiten der 0.6m Schwelle
            if distance <= self.start_threshold and not self.measurement_started and distance > self.stop_threshold:
                self.start_time = time.time()
                self.measurement_started = True
                self.get_logger().info("0.6m Grenze durchstoßen - Zeitmessung gestartet.")

            # Stoppbedingung: Unterschreiten der 0.5m Schwelle
            elif distance <= self.stop_threshold and self.measurement_started:
                end_time = time.time()
                duration = end_time - self.start_time
                self.measurement_started = False

                # Strecke zwischen 0.6m und 0.5m (0.1m)
                Strecke_in_Meter = 0.1
                Geschwindigkeit = Strecke_in_Meter / duration  # m/s
                Geschwindigkeit_kmh = Geschwindigkeit * 3.6    # in km/h

                self.get_logger().info(f"Geschwindigkeit: {Geschwindigkeit_kmh:.2f} km/h (Zeit: {duration:.3f} s)")

                # Nach Messung keine weiteren Aktionen bis neue Startbedingung
                break


def main(args=None):
    rclpy.init(args=args)
    node = SpeedDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

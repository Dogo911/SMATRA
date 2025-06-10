import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import time

class SpeedDetector(Node):
    def __init__(self):
        super().__init__('speed_detector')

        # Subscriben auf das LaserScan-Topic
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)

        # Parameter
        self.detect_distance_min = 0.5  # Mindestabstand zur Erkennung [Meter]
        self.detect_distance_max = 0.6  # Maximalabstand zur Erkennung [Meter]
        self.detect_angle_min = -15      # Winkelbereich links [-5°]
        self.detect_angle_max = 15        # Winkelbereich rechts [+5°]

        self.object_detected = False
        self.start_time = None

    def scan_callback(self, msg):
        # Anzahl der Messpunkte
        num_points = len(msg.ranges)

        # Scanwinkel Bereich bestimmen
        angle_min = msg.angle_min
        angle_max = msg.angle_max
        angle_increment = msg.angle_increment

        # Indizes für den gewünschten Winkelbereich berechnen
        index_min = int((self.detect_angle_min * 3.1415/180.0 - angle_min) / angle_increment)
        index_max = int((self.detect_angle_max * 3.1415/180.0 - angle_min) / angle_increment)

        # Safety: Grenzen abfangen
        index_min = max(0, min(num_points-1, index_min))
        index_max = max(0, min(num_points-1, index_max))

        # Bereich herausfiltern
        region = msg.ranges[index_min:index_max]

        # Prüfen, ob ein Objekt im definierten Bereich liegt
        for distance in region:
            if self.detect_distance_min < distance < self.detect_distance_max:
                if not self.object_detected:
                    self.object_detected = True
                    self.start_time = time.time()
                    self.get_logger().info("Objekt entdeckt - Messung gestartet.")
                return
        
        # Falls vorher Objekt da war, aber jetzt nicht mehr
        if self.object_detected:
            end_time = time.time()
            duration = end_time - self.start_time
            self.object_detected = False

            # Strecke definieren (z.B. 1 Meter Abstand)
            Strecke_in_Meter = 0.1
            Geschwindigkeit = Strecke_in_Meter / duration  # m/s
            Geschwindigkeit_kmh = Geschwindigkeit * 3.6    # umrechnen in km/h

            self.get_logger().info(f"Geschwindigkeit: {Geschwindigkeit_kmh:.2f} km/h")

def main(args=None):
    rclpy.init(args=args)
    node = SpeedDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

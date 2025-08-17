#!/usr/bin/env python3
import time
import math
from enum import Enum

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from twist_mux_msgs.action import JoyTurbo
from rclpy.action import ActionClient
from visualization_msgs.msg import Marker, MarkerArray


class State(Enum):
    FREE = 0
    DANGER = 2


class SafetyStop(Node):
    def __init__(self):
        super().__init__('safety_stop_node')
        
        self.declare_parameter('danger_distance', 0.4)
        self.declare_parameter('scan_topic', 'scan')
        self.declare_parameter('safety_stop_topic', 'safety_stop')
        self.danger_distance = self.get_parameter('danger_distance').get_parameter_value().double_value
        self.scan_topic = self.get_parameter('scan_topic').get_parameter_value().string_value
        self.safety_stop_topic = self.get_parameter('safety_stop_topic').get_parameter_value().string_value
        self.laser_sub = self.create_subscription(
            LaserScan, self.scan_topic, self.laser_callback, 10
        )
        self.safety_stop_pub = self.create_publisher(
            Bool, self.safety_stop_topic, 10
        )
        self.state = State.FREE
        
    def laser_callback(self, msg: LaserScan):
        self.state = State.FREE

        for range_value in msg.ranges:

            if not math.isinf(range_value) and range_value <= self.danger_distance:

                
                self.state = State.DANGER
                    # Stop immediately!
                break

        
        is_safety_stop = Bool()

        
        if self.state == State.DANGER:
                is_safety_stop.data = True
                
        elif self.state == State.FREE:
            is_safety_stop.data = False
            
        self.safety_stop_pub.publish(is_safety_stop)

        

        


def main():
    rclpy.init()
    node = SafetyStop()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

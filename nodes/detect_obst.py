import numpy as np
import rospy
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
import time

class ObstacleDetect():

    def __init__(self):
        self.sub = rospy.Subscriber("/scan",LaserScan, self.callback)
        self.pub = rospy.Publisher("/pos_obst", Point, queue_size=10)
        rospy.init_node('detect_obst', anonymous=True)
        self.rate = rospy.Rate(2)
        self.msg = Point()
        self.scan = LaserScan()

    def callback(self, data):
        self.scan = data

    def RAD2DEG(self, x):
        return (x*180.)/np.pi

    def run(self):
        while not rospy.is_shutdown():
            if not (len(self.scan.ranges)==0):
                rospy.loginfo('ObstacleDetect boucle :')
                self.dist_min = min(self.scan.ranges[180:360])
                if dist_min < 1.5:
                    self.msg.x = self.dist_min
                    self.msg.y = self.RAD2DEG(self.scan.angle_min + self.scan.ranges.index(min(self.dist_min))*self.scan.angle_increment)
                    self.msg.z = 1
                    self.pub.publish(self.msg)
                    loginfo("L'obstacle est a {1}m et {2}deg".format(self.msg.x, self.msg.y))
                else:
                    self.msg.x = 0
                    self.msg.y = 0
                    self.msg.z = 0
                    self.pub.publish(self.msg)
                    loginfo("Pas d'obstacle")

test = ObstacleDetect()
test.run()

#pour rendre le code executable :
#chmod u+x ~/catkin_ws/src/turtlesim_cleaner/src/move.py

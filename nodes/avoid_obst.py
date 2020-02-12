import numpy as np
import rospy
from geometry_msgs.msg import Point
from geometry_msgs.msg import TwistStamped
from mavros_msgs.srv import *
import time

class ObstacleAvoid():
    def __init__(self):
        self.sub = rospy.Subscriber("/pos_obst", Point, self.callback)
        self.pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel", TwistStamped, queue_size=10)
        self.mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
        rospy.init_node('test_vel', anonymous=True)
        self.rate = rospy.Rate(2)
        self.msg = TwistStamped()

    def callback(self, data):
        self.scan = data
        if self.scan.z == 1:
            if not self.resultatMode:
                self.resultatMode = self.mode(216, 'GUIDED')
                logwarn("Mode GUIDED !")
        else :
            if self.resultatMode:
                self.resultatMode = not (self.mode(220, 'AUTO'))
                logwarn("Mode AUTO !")

    def cmd_vit(self, point):
        #point.x = distance dist_min
        #point.y = angle deg
        #return angulaire z (+ gauche, - droite), linear x
        if point.x > 1 : #zone 2
            if point.y < 60 : #zone D
                return 0.0, 5.0
            if point.y < 90 : #zone C
                return 5.0, 4.0
            elif point.y < 120 : #zone B
                return -5.0, 4.0
            else: #zone A
                return 0.0, 5.0
        elif point.x > 0.5 :#zone1
            if point.y < 60 : #zone D
                return 0.0, 5.0
            elif point.y < 90 : #zone C
                return 5.0, 2.0
            elif point.y < 120 : #zone B
                return -5.0, 2.0
            else: #zone A
                return 0.0, 5.0
        else : #zone0
            if point.y < 60 : #zone D
                return 0.0, 5.0
            elif point.y < 90 : #zone C
                return 5.0, 0.
            elif point.y < 120 : #zone B
                return -5.0, 0.0
            else: #zone A
                return 0.0, 5.0

    def run(self):
        while not rospy.is_shutdown():
                self.msg.twist.angular.x = 0
                self.msg.angular.y = 0
                self.msg.linear.y = 0
                self.msg.linear.z = 0
                self.msg.angulaire.z, self.msg.linear.x = cmd_vit(self.scan)
                self.pub.publish(self.msg)
                loginfo("linear : {}, angular : {}".format(self.msg.angulaire.z, self.msg.linear.x))

test = ObstacleAvoid()
test.run()

import numpy as np
import rospy
from geometry_msgs.msg import Point
from geometry_msgs.msg import TwistStamped
from mavros_msgs.srv import *
import time

class TestVelocity():
    def __init__(self):
        self.pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel", TwistStamped, queue_size=10)
        self.mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
        rospy.init_node('avoid_obst', anonymous=True)
        self.rate = rospy.Rate(2)
        self.msg = TwistStamped()
        self.resultat = False

    def run(self):
        while not rospy.is_shutdown():
            if not self.resultat:
                self.resultat = self.mode(216, 'GUIDED')
                
            self.msg.twist.angular.x = 0
            self.msg.angular.y = 0
            self.msg.linear.y = 0
            self.msg.linear.z = 0
            self.msg.angulaire.z, self.msg.linear.x = input("vit ang & vit lin : ")
            loginfo("linear : {}, angular : {}".format(self.msg.angulaire.z, self.msg.linear.x))
            self.pub.publish(self.msg)

test = TestVelocity()
test.run()

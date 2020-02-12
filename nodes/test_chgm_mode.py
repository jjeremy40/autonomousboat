import numpy as np
import rospy
from geometry_msgs.msg import Point
from geometry_msgs.msg import TwistStamped
import time

class TestMode():
    def __init__(self):
        self.mode = rospy.ServiceProxy('/mavros/set_mode')
        rospy.init_node('test_chgm_mode', anonymous=True)
        self.rate = rospy.Rate(2)
        self.resultatMode = 0

    def run():
        while not rospy.is_shutdown():
            self.resultatMode = self.mode(216, 'GUIDED')
            if self.resultatMode == 1 :
                loginfo("Mode : GUIDED")
            else:
                loginfo("Mode : not GUIDED")

test = TestMode()
test.run()

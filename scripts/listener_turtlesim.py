#!/usr/bin/env python  
import roslib
roslib.load_manifest('state_machines')
import rospy
import math
import tf
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import turtlesim.srv

if __name__ == '__main__':

    rospy.init_node('listener_turtlesim')
    listener = tf.TransformListener()
    velocity_publisher = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
    cmd = Twist(); cmd.linear.x = 0.1

    timeout = 1.0
    rate = rospy.Rate(10.0)
    # The control of the State Machine is all done inside the following loop
    while not rospy.is_shutdown():

        # We try to take the transform between /world and /tartaruga. 
        # If it does not exists, inside the "timeout" interval, the node should move on
        try:
            now = rospy.Time()
            listener.waitForTransform("/world", "/tartaruga", now, rospy.Duration(timeout))
            (trans, rot) = listener.lookupTransform("/world", "/tartaruga", now)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        # settings STATES, which means SETS OF CONDITIONS
        if(trans[0] < 6.0): state = 'A'
        elif(trans[0] < 7.0): state = 'B'
        else: state = 'off'

        print 'trans[0]: ', trans[0]
        print 'trans[1]: ', trans[1]
        print 'state: ', state
        velocity_publisher.publish(cmd)

        rate.sleep()



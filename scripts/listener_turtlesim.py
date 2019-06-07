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

    timeout = 0.048  # timeout here is chosen (arbitrarilly) 3 times "input msg interval", which is 1/62.5Hz = 0.016.  Then, 3 x 0.016 = 0.048
    rate = rospy.Rate(10.0)
    # The control of the State Machine is all done inside the following loop
    while not rospy.is_shutdown():

        # We try to take the transform between /world and /tartaruga. 
        # If it does not exists, inside the "timeout" interval, the node should move on
        try:
            now = rospy.Time()
            listener.waitForTransform("/world", "/tartaruga", now, rospy.Duration(timeout))
            (trans, rot) = listener.lookupTransform("/world", "/tartaruga", now)
        #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        except:
            rospy.loginfo("There is no transform!")

            continue


        cmd = Twist()
        print 'trans[0]: ', trans[0]

        # settings STATES, which means SETS OF CONDITIONS
        if(trans[0] < 6.0): 
            #state = 'A'
            cmd.linear.x = 0.1
            cmd.angular.z = 0.0
        elif(trans[0] < 7.5): 
            #state = 'B'
            cmd.linear.x = 0.1
            cmd.angular.z = 0.03
        else: 
            #state = 'off'
            cmd.linear.x = 0.0
            cmd.angular.z = 0.1

        velocity_publisher.publish(cmd)
        rate.sleep()



#!/usr/bin/env python  
import roslib
roslib.load_manifest('state_machines')
import rospy

import tf
import turtlesim.msg

import random

'''
    This secondary version of broadcaster splits the incoming data as event-driven
    in the callback function and send the tf's separately. 
    The advantage of doing this is that you can set a different 
    frequency rate (minor, major,...).
'''

x = 0
y = 0
theta = 0

def handle_turtle_pose(msg):
    global x, y, theta
    x = msg.x
    y = msg.y
    theta = msg.theta
    # This msg comes as event-driven data, which means, 
    # at the frequency of whichever are publishing.
    print "msg.x: ", msg.x, "msg.y: ", msg.y

if __name__ == '__main__':
    rospy.init_node('broadcaster_turtlesim')

    rospy.Subscriber('/turtle1/pose', turtlesim.msg.Pose, handle_turtle_pose)

    initial_time = rospy.get_time()
    print "Broadcaster running..."

    # Here, we can define another frequency of publishing
    rate = rospy.Rate(121)
    while not rospy.is_shutdown():
        br = tf.TransformBroadcaster()
        br.sendTransform((x, y, 0),
tf.transformations.quaternion_from_euler(0, 0, theta),
                     rospy.Time.now(),
                     "tartaruga",
                     "world")
        print "some data being sent/published at the above rate frequency!"
        #print "You could also not use rospy.rate()/rate.sleep(), what means your data would be sent/published at asynchronous SO process rate!"

        rate.sleep()
        # simulate some noise! This causes a bottleneck effect!
        rospy.sleep(random.random())


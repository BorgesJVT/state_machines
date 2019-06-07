#!/usr/bin/env python  
import roslib
roslib.load_manifest('state_machines')
import rospy

import tf
import turtlesim.msg

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

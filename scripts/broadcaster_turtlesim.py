#!/usr/bin/env python  
import roslib
roslib.load_manifest('state_machines')
import rospy

import tf
import turtlesim.msg

def handle_turtle_pose(msg):
    br = tf.TransformBroadcaster()
    print "msg.x: ", msg.x, "msg.y: ", msg.y
    #rospy.sleep(0.5)
    br.sendTransform((msg.x, msg.y, 0),
                     tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                     rospy.Time.now(),
                     "tartaruga",
                     "world")

if __name__ == '__main__':
    rospy.init_node('broadcaster_turtlesim')

    rospy.Subscriber('/turtle1/pose', turtlesim.msg.Pose, handle_turtle_pose)
    print "Broadcaster running..."

    rospy.spin()

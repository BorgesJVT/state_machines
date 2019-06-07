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
    '''
    Parameters:
      *  name (str)                     - Graph resource name of topic, e.g. 'turtle1/pose'.

      *  data_class (Message class)     - Data type class to use for messages, e.g. std_msgs.msg.String

      *  callback (fn(msg, cb_args))    - Function to call ( fn(data)) when data is received. If callback_args is set, 
                                          the function must accept the callback_args as a second argument, 
                                          i.e. fn(data, callback_args). 
                                          NOTE: Additional callbacks can be added using add_callback().

      *  callback_args (any)            - Additional arguments to pass to the callback. 
                                          This is useful when you wish to reuse the same callback for multiple subscriptions.

      *  queue_size (int)               - Maximum number of messages to receive at a time. 
                                          This will generally be 1 or None (infinite, default). 
                                          buff_size should be increased if this parameter is set as incoming data 
                                          still needs to sit in the incoming buffer before being discarded. 
                                          Setting queue_size buff_size to a non-default value affects all subscribers 
                                          to this topic in this process.
      *  buff_size (int)                - Incoming message buffer size in bytes. If queue_size is set, 
                                          this should be set to a number greater than the queue_size times 
                                          the average message size. 
                                          Setting buff_size to a non-default value affects all subscribers 
                                          to this topic in this process.
      * tcp_nodelay (bool)              - if True, request TCP_NODELAY from publisher. Use of this option is not generally recommended in most cases as it is better to rely on timestamps in message data. Setting tcp_nodelay to True enables TCP_NODELAY for all subscribers in the same python process.

    '''
    rospy.Subscriber('/turtle1/pose', turtlesim.msg.Pose, handle_turtle_pose)
    print "Broadcaster running..."

    rospy.spin()

#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from smach import CBState
        

@smach.cb_interface(input_keys=[], output_keys=[], outcomes=['finished','failed'])
def takeoff_cb( user_data):
    rospy.loginfo('Taking Off')
    takeoff_topic = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
    rospy.sleep(1)
    msg = Empty()
    result = takeoff_topic.publish(msg)
    if result == None:
        return 'finished'
    else:
        return 'failed'

@smach.cb_interface(input_keys=[], output_keys=[], outcomes=['finished','failed'])
def land_cb( user_data):
    rospy.loginfo('Landing')
    land_topic = rospy.Publisher('/drone/land', Empty, queue_size=1)
    rospy.sleep(1)
    msg = Empty()
    result = land_topic.publish(msg)
    if result == None:
        return 'finished'
    else:
        return 'failed'
        
@smach.cb_interface(input_keys=['lspeed'], output_keys=[], outcomes=['finished','failed'])
def move_cb( user_data):
    rospy.loginfo('Moving')
    cmd_topic = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.sleep(1)
    vel = Twist()
    vel.linear.x = user_data.lspeed
    result = cmd_topic.publish(vel)
    rospy.sleep(2)
    if result == None:
        return 'finished'
    else:
        return 'failed'

@smach.cb_interface(input_keys=['rspeed'], output_keys=[], outcomes=['finished','failed'])
def rotate_cb( user_data):
    rospy.loginfo('Rotating')
    cmd_topic = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.sleep(1)
    vel = Twist()
    vel.angular.z = user_data.rspeed
    result = cmd_topic.publish(vel)
    rospy.sleep(2)
    if result == None:
        return 'finished'
    else:
        return 'failed'

if __name__ == '__main__':
    
    rospy.init_node('drone_state_machine')
    
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome'])
    sm.userdata.lspeed = 0.5
    sm.userdata.rspeed = 1.2
    
    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('drone_server', sm, '/SM_DRONE')
    sis.start()

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('TAKEOFF', CBState(takeoff_cb),
                               {'finished': 'MOVE', 'failed':'outcome'})
        smach.StateMachine.add('MOVE', CBState(move_cb),
                               {'finished': 'ROTATE', 'failed':'outcome'})
        smach.StateMachine.add('ROTATE', CBState(rotate_cb),
                               {'finished': 'LAND', 'failed':'outcome'})
        smach.StateMachine.add('LAND', CBState(land_cb),
                               {'finished': 'outcome', 'failed':'outcome'})
        

    # Execute SMACH plan
    outcome = sm.execute()
    
    sis.stop()

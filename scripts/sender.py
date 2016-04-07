#!/usr/bin/env python
__author__ = 'flier and stefan spiss'

import argparse

import rospy
import leap_interface
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float32

FREQUENCY_ROSTOPIC_DEFAULT = 0.1
PARAMNAME_FREQ = '/leapmotion/freq'

# This method publishes hand data detected from the leap motion to the topics /leapmotion/pose,
# /leapmotion/direction, /lepmotion/normal and /leapmotion/grabA
def sender(freq=FREQUENCY_ROSTOPIC_DEFAULT):
    '''
    @param freq: Frequency to publish sensed info as ROS message
    '''
    rospy.set_param(PARAMNAME_FREQ, freq)
    rospy.loginfo("Parameter set on server: PARAMNAME_FREQ={}, freq={}".format(rospy.get_param(PARAMNAME_FREQ, FREQUENCY_ROSTOPIC_DEFAULT), freq))

    li = leap_interface.Runner()
    li.setDaemon(True)
    li.start()

    pub_pose    = rospy.Publisher('leapmotion/pose', Pose, queue_size=1)
    pub_dir     = rospy.Publisher('leapmotion/direction', Vector3, queue_size=1)
    pub_normal  = rospy.Publisher('leapmotion/normal', Vector3, queue_size=1)
    pub_grab    = rospy.Publisher('leapmotion/grab', Float32, queue_size=1)
    
    rospy.init_node('leap_pub')

    while not rospy.is_shutdown():             
        hand_direction_   = li.get_hand_direction()
        hand_normal_      = li.get_hand_normal()
        hand_palm_pos_    = li.get_hand_palmpos()
        hand_pitch_       = li.get_hand_pitch()
        hand_roll_        = li.get_hand_roll()
        hand_yaw_         = li.get_hand_yaw()
        hand_grab_        = li.get_hand_grab_strength()
        
        # Hand pose msg
        pose_msg = Pose()
        pose_msg.position.x = hand_palm_pos_[0]
        pose_msg.position.y = hand_palm_pos_[1]
        pose_msg.position.z = hand_palm_pos_[2]
        pose_msg.orientation.x = hand_pitch_
        pose_msg.orientation.y = hand_yaw_
        pose_msg.orientation.z = hand_roll_
        
        # Hand direction msg
        dir_msg = Vector3()
        dir_msg.x = hand_direction_[0]
        dir_msg.y = hand_direction_[1]
        dir_msg.z = hand_direction_[2]
        
        # Hand normal msg
        norm_msg = Vector3()
        norm_msg.x = hand_normal_[0]
        norm_msg.y = hand_normal_[1]
        norm_msg.z = hand_normal_[2]
        
        # Grab strength msg
        grab_msg = Float32()
        grab_msg = hand_grab_
        
        # Publish
        pub_pose.publish(pose_msg)
        pub_dir.publish(dir_msg)
        pub_normal.publish(norm_msg)
        pub_grab.publish(grab_msg)
        rospy.sleep(rospy.get_param(PARAMNAME_FREQ, FREQUENCY_ROSTOPIC_DEFAULT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LeapMotion ROS driver. Message Sender module to ROS world using LeapSDK.')
    parser.add_argument('--freq', help='Frequency to publish sensed info as ROS message', type=float)
    args, unknown = parser.parse_known_args()
    if not args.freq:
        args.freq = FREQUENCY_ROSTOPIC_DEFAULT
    try:
        sender(args.freq)
    except rospy.ROSInterruptException:
        pass

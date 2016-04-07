#################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.                #
# Leap Motion proprietary and confidential. Not for distribution.               #
# Use subject to the terms of the Leap Motion SDK Agreement available at        #
# https://developer.leapmotion.com/sdk_agreement, or another agreement          #
# between Leap Motion and you, your company or other organization.              #
#################################################################################

#################################################################################
# Altered LEAP example by Florian Lier and Stefan Spiss, you need to have the   #
# LEAP SDK installed for this to work properly.                                 #
# This interface provides access to the LEAP MOTION hardware, you will need to  #
# have the official LEAP MOTION SDK installed in order to load the shared       #
# provided with the SDK.                                                        #
#################################################################################

import sys
import time
# Set (append) your PYTHONPATH properly, or just fill in the location of your LEAP
# SDK folder, e.g., $HOME/LeapSDK/lib where the Leap.py lives and /LeapSDK/lib/x64 or
# x86 where the *.so files reside.

# Below, you can see the "dirty" version - NOT RECOMMENDED!

#sys.path.append("/home/LeapDeveloperKit_2.3.1+31549_linux/LeapSDK/lib")
#sys.path.append("/home/LeapDeveloperKit_2.3.1+31549_linux/LeapSDK/lib/x64")
import threading
import Leap

class LeapInterface(Leap.Listener):
    def on_init(self, controller):
        # These variables as probably not thread safe
        # TODO: Make thread safe ;)
        self.hand           = [0,0,0]
        self.right_hand = False
        self.left_hand = False
        self.hand_direction = [-10,-10,-10]
        self.hand_normal    = [0,0,0]
        self.hand_palm_pos  = [0,0,0]
        self.hand_pitch     = -10.0
        self.hand_yaw       = -10.0
        self.hand_roll      = -10.0
        self.grab           = -1.0
        print "Initialized Leap Motion Device"

    def on_connect(self, controller):
        print "Connected to Leap Motion Controller"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected Leap Motion"

    def on_exit(self, controller):
        print "Exited Leap Motion Controller"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

#         print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
#              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        
        if frame.hands.is_empty:
            self.hand           = [0,0,0]
            self.right_hand = False
            self.left_hand = False
            self.hand_direction = [-10,-10,-10]
            self.hand_normal    = [0,0,0]
            self.hand_palm_pos  = [0,0,0]
            self.hand_pitch     = -10.0
            self.hand_yaw       = -10.0
            self.hand_roll      = -10.0
            self.grab           = -1.0
        
        else: #recently changed in API
            # Get the first hand
            #we are seeking one left and one right hands
            there_is_right_hand=False
            there_is_left_hand=False
            
            for hand in frame.hands:
            
                if hand.is_right:
                    there_is_right_hand=True
                    self.right_hand=hand
                elif hand.is_left:
                    there_is_left_hand=True
                    
                    self.left_hand=hand
            
            if not there_is_right_hand:
                self.right_hand=False
            
            if not there_is_left_hand:
                self.left_hand=False
                        
            self.hand = frame.hands[0] #old way

            # Check if the hand has any fingers
            #fingers = self.hand.fingers
            #if not fingers.empty:
                # Calculate the hand's average finger tip position
                #avg_pos = Leap.Vector()
                #for finger in fingers:
                    #avg_pos += finger.tip_position
                # avg_pos /= len(fingers)
                # print "Hand has %d fingers, average finger tip position: %s" % (len(fingers), avg_pos)

            # Get the hand's sphere radius and palm position
            #print "Hand sphere radius: %f" % (self.hand.pinch_strength)

            # Get the hand's normal vector and direction
            normal = self.hand.palm_normal
            direction = self.hand.direction
            pos = self.hand.palm_position

            self.hand_direction[0] = direction.x
            self.hand_direction[1] = direction.y
            self.hand_direction[2] = direction.z
            self.hand_normal[0]    = normal.x
            self.hand_normal[1]    = normal.y
            self.hand_normal[2]    = normal.z
            self.hand_palm_pos[0]  = pos.x
            self.hand_palm_pos[1]  = pos.y
            self.hand_palm_pos[2]  = pos.z
            self.hand_pitch        = direction.pitch
            self.hand_yaw          = direction.yaw
            self.hand_roll         = normal.roll
            
            self.grab              = self.hand.grab_strength
            # Calculate the hand's pitch, roll, and yaw angles
          #  print "Hand pitch: %f radiant, roll: %f rad, yaw: %f rad" % (self.hand_pitch, self.hand_roll, self.hand_yaw)

    def get_hand_direction(self):
        return self.hand_direction

    def get_hand_normal(self):
        return self.hand_normal

    def get_hand_palmpos(self):
        return self.hand_palm_pos

    def get_hand_yaw(self):
        return self.hand_yaw

    def get_hand_pitch(self):
        return self.hand_pitch

    def get_hand_roll(self):
        return self.hand_roll
    
    def get_hand_grab_strength(self):
        return self.grab


class Runner(threading.Thread):

    def __init__(self,arg=None):
        threading.Thread.__init__(self)
        self.arg=arg
        self.listener = LeapInterface()
        self.controller = Leap.Controller()
        self.controller.add_listener(self.listener)
    
    def __del__(self):
        self.controller.remove_listener(self.listener)

    def get_hand_direction(self):
        return self.listener.get_hand_direction()

    def get_hand_normal(self):
        return self.listener.get_hand_normal()

    def get_hand_palmpos(self):
        return self.listener.get_hand_palmpos()

    def get_hand_roll(self):
        return self.listener.get_hand_roll()

    def get_hand_pitch(self):
        return self.listener.get_hand_pitch()

    def get_hand_yaw(self):
        return self.listener.get_hand_yaw()
    
    def get_hand_grab_strength(self):
        return self.listener.get_hand_grab_strength()

    def run (self):
        while True:
            # Save some CPU time
            time.sleep(0.001)


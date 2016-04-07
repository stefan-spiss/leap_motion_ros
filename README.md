# leap_motion_ros
Simple ROS node that publishes data detected by the Leap Motion.

For the implementation the ROS node from Florian Lier which is available at [https://github.com/warp1337/rosleapmotion](https://github.com/warp1337/rosleapmotion) was adapted. 

## Changes made
- Everything expect of the **sender.py** and the **leap_interface.py** removed.
- Changed **publisher** in **sender.py** from publishing self-defined messages to publishing messages of pre-defined message types.
- In the **leap_interface.py** code for accessing the Leap Motion gestures and the fingers was removed. Furthermore, the way how the hand angles are obtained was changed according to the Leap Motion website. Code to retrieve the hand's grab strength was also added.

## Node
The only node **sender.py** publishes sensor data otained with the Leap Motion to the following topics:
- **/leapmotion/direction** for hand direction
- **/leapmotion/normal** for the palm normal
- **/leapmotion/pose** pose of the hand
- **/leapmotion/grab** grab strength of the hand

## Setup
The Leap Motion SDK need to be downloaded and either added to the **PYTHONPATH** or hardcoded set in the **leap_interface.py** file. Additionally, also the **leapd** service must run while using the ROS node.

cmake_minimum_required(VERSION 2.8.3)
project(leap_motion_ros)

find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs geometry_msgs)

catkin_package(
   CATKIN_DEPENDS roscpp rospy std_msgs 
)

include_directories(include
  ${catkin_INCLUDE_DIRS}
)

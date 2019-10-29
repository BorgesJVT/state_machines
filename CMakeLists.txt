cmake_minimum_required(VERSION 2.8.3)
project(state_machines_smach_ROS)

find_package(catkin REQUIRED)

## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
catkin_python_setup()

catkin_package()

include_directories()

#############
## Install ##
#############

install(PROGRAMS
   scripts/basic_example.py
   scripts/drone_example.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


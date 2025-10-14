cmake_minimum_required(VERSION 3.22)
project(melfa_rv2fr_gripper_moveit_config)

set(THIS_PACKAGE_INCLUDE_DEPENDS
  ament_cmake
  rclcpp
  rclcpp_action
  tf2_geometry_msgs
  control_msgs
)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(control_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)


ament_package()

install(DIRECTORY launch config rviz DESTINATION share/${PROJECT_NAME})


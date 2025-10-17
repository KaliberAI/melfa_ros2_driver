#    COPYRIGHT (C) 2024 Mitsubishi Electric Corporation

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    # Declare arguments

    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            'start_rviz',
            default_value='true',
            description='Start RViz2 automatically with this launch file.',
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "moveit_config_package",
            default_value="melfa_rv2fr_moveit_config",
            description="MoveIt config package with robot SRDF/XACRO files. Usually the argument \
        is not set, it enables use of a custom moveit config.",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Using or not time from simulation",
        )
    )

    # Initialize Arguments
    start_rviz = LaunchConfiguration('start_rviz')
    moveit_config_package = LaunchConfiguration("moveit_config_package")
    use_sim_time = LaunchConfiguration("use_sim_time")

    # Initialize Moveit Configuration
    moveit_config = (
        MoveItConfigsBuilder("rv2fr", package_name="melfa_rv2fr_moveit_config")
        .robot_description(file_path="config/rv2fr.urdf.xacro")
        .robot_description_semantic(file_path="config/rv2fr.srdf.xacro")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .planning_pipelines(
            # pipelines=["ompl", "chomp", "pilz_industrial_motion_planner", "stomp"] # Add "stomp" if moveit2 humble branch adds stomp feature
            pipelines=["ompl", "chomp", "pilz_industrial_motion_planner"]
        )
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .joint_limits(file_path="config/joint_limits.yaml")
        .pilz_cartesian_limits(file_path="config/pilz_cartesian_limits.yaml")
        .to_moveit_configs()
    )
    

    # Start the actual move_group node/action server
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {
                "use_sim_time": use_sim_time,
            },
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # rviz with moveit configuration
    rviz_config_file = PathJoinSubstitution(
        [get_package_share_directory("melfa_rv2fr_moveit_config"), "rviz", "rv2fr_moveit.rviz"]
    )
    rviz_node = Node(
        package="rviz2",
        condition=IfCondition(start_rviz),
        executable="rviz2",
        name="rviz2_moveit",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            {
                "use_sim_time": use_sim_time,
            },
        ],
    )

    nodes = [move_group_node, rviz_node]

    return LaunchDescription(declared_arguments + nodes)

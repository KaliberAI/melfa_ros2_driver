from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Build MoveIt configuration
    moveit_config = (
        MoveItConfigsBuilder("RV2FR", package_name="melfa_rv2fr_moveit_config")
        .robot_description(file_path="config/rv2fr_gripper.urdf.xacro")
        .robot_description_semantic(file_path="config/rv2fr_gripper.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )
    
    # Declare arguments
    declared_arguments = []
    
    declared_arguments.append(
        DeclareLaunchArgument(
            'allow_trajectory_execution',
            default_value='true',
            description='Allow trajectory execution'
        )
    )
    
    declared_arguments.append(
        DeclareLaunchArgument(
            'publish_monitored_planning_scene',
            default_value='true',
            description='Publish monitored planning scene'
        )
    )
    
    # Generate move_group launch
    move_group_launch = generate_move_group_launch(moveit_config)
    
    # Add RViz with MoveIt plugin
    rviz_config = moveit_config.package_path / "config/moveit.rviz"
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_moveit',
        output='log',
        arguments=['-d', str(rviz_config)],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
        ],
    )
    
    return LaunchDescription(
        declared_arguments + 
        move_group_launch.entities
        #[rviz_node]
    )

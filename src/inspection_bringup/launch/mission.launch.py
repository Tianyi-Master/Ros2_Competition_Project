"""Launch the mission state machine and parking controller."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='mission_controller',
            executable='mission_server',
            name='mission_server',
            output='screen',
        ),
        Node(
            package='mission_controller',
            executable='parking_controller',
            name='parking_controller',
            output='screen',
        ),
    ])

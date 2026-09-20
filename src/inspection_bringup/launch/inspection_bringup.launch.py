"""Top-level bringup for the inspection robot.

Launches perception + mission by default. Set ``nav:=true`` to also bring up
AMCL + the Nav2 navigation stack (requires the Nav2 packages and a map).
"""

import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('inspection_bringup')
    launch_dir = os.path.join(share_dir, 'launch')

    nav = LaunchConfiguration('nav')

    return LaunchDescription([
        DeclareLaunchArgument('nav', default_value='false',
                              description='Enable AMCL + Nav2 navigation stack'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'perception.launch.py'))),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'mission.launch.py'))),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'amcl.launch.py')),
            condition=IfCondition(nav)),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'navigation.launch.py')),
            condition=IfCondition(nav)),
    ])

"""Navigation stack (Nav2) with laser scan input.

Launches the standard Nav2 node set driven by ``config/nav2_params.yaml``.
Requires the Nav2 packages to be installed. Combine with ``amcl.launch.py``
(or ``slam.launch.py`` while mapping) for localization.
"""

import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('inspection_bringup')
    nav2_params = os.path.join(share_dir, 'config', 'nav2_params.yaml')

    map_yaml = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        DeclareLaunchArgument('map', default_value=os.path.join(share_dir, 'maps', 'map.yaml')),
        DeclareLaunchArgument('use_sim_time', default_value='false'),

        # Map server (shared with AMCL if launched in the same session).
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'yaml_filename': map_yaml, 'use_sim_time': use_sim_time}],
        ),

        Node(package='nav2_controller', executable='controller_server', name='controller_server',
             output='screen', parameters=[nav2_params, {'use_sim_time': use_sim_time}]),
        Node(package='nav2_planner', executable='planner_server', name='planner_server',
             output='screen', parameters=[nav2_params, {'use_sim_time': use_sim_time}]),
        Node(package='nav2_behaviors', executable='behavior_server', name='behavior_server',
             output='screen', parameters=[nav2_params, {'use_sim_time': use_sim_time}]),
        Node(package='nav2_bt_navigator', executable='bt_navigator', name='bt_navigator',
             output='screen', parameters=[nav2_params, {'use_sim_time': use_sim_time}]),
        Node(package='nav2_waypoint_follower', executable='waypoint_follower', name='waypoint_follower',
             output='screen', parameters=[nav2_params, {'use_sim_time': use_sim_time}]),
        Node(package='nav2_velocity_smoother', executable='velocity_smoother', name='velocity_smoother',
             output='screen', parameters=[nav2_params, {'use_sim_time': use_sim_time}]),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'autostart': True,
                'node_names': [
                    'controller_server', 'planner_server', 'behavior_server',
                    'bt_navigator', 'waypoint_follower', 'velocity_smoother',
                ],
            }],
        ),
    ])

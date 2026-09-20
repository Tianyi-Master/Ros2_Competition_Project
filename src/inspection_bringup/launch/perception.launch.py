"""Launch all perception nodes (8 tasks)."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    camera_rgb = LaunchConfiguration('camera_rgb_topic')
    camera_thermal = LaunchConfiguration('camera_thermal_topic')

    # (executable, node_name, result_topic) for RGB-based tasks.
    rgb_tasks = [
        ('traffic_light', 'traffic_light_node', '/perception/traffic_light'),
        ('crowd', 'crowd_node', '/perception/crowd'),
        ('bin_status', 'bin_status_node', '/perception/bin_status'),
        ('fire', 'fire_node', '/perception/fire'),
        ('license_plate', 'license_plate_node', '/perception/license_plate'),
        ('meter', 'meter_node', '/perception/meter'),
        ('ev_status', 'ev_status_node', '/perception/ev_status'),
    ]

    actions = [
        DeclareLaunchArgument('camera_rgb_topic', default_value='/camera/image_raw'),
        DeclareLaunchArgument('camera_thermal_topic', default_value='/thermal/image_raw'),
    ]

    for exe, name, result_topic in rgb_tasks:
        actions.append(Node(
            package='perception',
            executable=exe,
            name=name,
            output='screen',
            parameters=[{'image_topic': camera_rgb, 'result_topic': result_topic}],
        ))

    # Temperature reads the thermal camera instead of the RGB camera.
    actions.append(Node(
        package='perception',
        executable='temperature',
        name='temperature_node',
        output='screen',
        parameters=[{'image_topic': camera_thermal, 'result_topic': '/perception/temperature'}],
    ))

    return LaunchDescription(actions)

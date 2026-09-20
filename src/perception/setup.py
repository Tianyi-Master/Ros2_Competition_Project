from setuptools import find_packages, setup

package_name = 'perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config',
            ['perception/config/models.yaml', 'perception/config/topics.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tianyimaster',
    maintainer_email='tianyimaster@todo.todo',
    description='Perception nodes for the inspection robot (YOLO + OpenCV).',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'traffic_light = perception.nodes.traffic_light_node:main',
            'crowd = perception.nodes.crowd_node:main',
            'bin_status = perception.nodes.bin_status_node:main',
            'fire = perception.nodes.fire_node:main',
            'license_plate = perception.nodes.license_plate_node:main',
            'temperature = perception.nodes.temperature_node:main',
            'meter = perception.nodes.meter_node:main',
            'ev_status = perception.nodes.ev_status_node:main',
        ],
    },
)

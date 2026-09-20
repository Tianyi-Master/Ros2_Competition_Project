from setuptools import find_packages, setup

package_name = 'mission_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tianyimaster',
    maintainer_email='tianyimaster@todo.todo',
    description='Patrol mission state machine and defined-position parking.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'mission_server = mission_controller.mission_server:main',
            'parking_controller = mission_controller.parking:main',
        ],
    },
)

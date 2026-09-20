cmake_minimum_required(VERSION 3.20)
project(inspection_bringup)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  launch
  config
  maps
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

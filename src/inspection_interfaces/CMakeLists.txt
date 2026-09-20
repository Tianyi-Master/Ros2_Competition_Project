cmake_minimum_required(VERSION 3.20)
project(inspection_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/BoundingBox2D.msg"
  "msg/Detection.msg"
  "msg/DetectionArray.msg"
  "msg/TrafficLight.msg"
  "msg/CrowdCount.msg"
  "msg/BinStatus.msg"
  "msg/FireEvent.msg"
  "msg/LicensePlate.msg"
  "msg/TemperatureReading.msg"
  "msg/MeterReading.msg"
  "msg/EVStatus.msg"
  "msg/InspectionAlert.msg"
  DEPENDENCIES std_msgs
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()

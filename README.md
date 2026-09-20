# 巡检机器人项目（Ros2 Competition Project）

基于 **YOLO + OpenCV + Nav2** 的 ROS 2 巡检机器人，集成多类感知任务与自主导航能力。

> 技术栈：ROS 2 **Lyrical** · Ubuntu 26.04 · YOLO (ultralytics) · OpenCV · Nav2 · slam_toolbox

## 功能

| 类别 | 功能 |
|---|---|
| 🚦 视觉感知 | 红绿灯识别 · 人群数量 · 垃圾桶满/未满 · 楼宇火灾（烟/光） · 车辆车牌 · 电动车状态（倒伏/违停） |
| 🌡️ 传感器 | 异常温度识别（热像仪） · 站房仪表读取 |
| 🧭 导航 | 激光 SLAM（slam_toolbox） · AMCL 定位 · 定义位置泊车 |
| 🤖 编排 | 巡检任务状态机（IDLE → PATROL → INSPECT → ALERT → PARK） |

## 快速开始

```bash
# 构建
cd Ros2_Competition_Project
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
source install/setup.bash

# 启动感知 + 任务编排（无需导航/硬件即可运行）
ros2 launch inspection_bringup inspection_bringup.launch.py

# 建图（需 slam_toolbox + 激光雷达）
ros2 launch inspection_bringup slam.launch.py

# 定位 + 导航（需 Nav2 + 地图文件）
ros2 launch inspection_bringup inspection_bringup.launch.py nav:=true
```

## 包结构

```
src/
├── inspection_interfaces/   # 自定义消息接口（12 个消息）
├── perception/              # 感知节点（8 个任务，YOLO + OpenCV）
├── mission_controller/      # 巡检状态机 + 定义位置泊车
└── inspection_bringup/      # launch + Nav2/SLAM/AMCL 配置
```

## 架构

```
传感器(RGB/热像/激光) → 感知节点 → /perception/* 结果话题
                                    ↓
                              巡检状态机(mission_server)
                                    ↓
                              Nav2 导航(巡检 + 泊车)
```

## 详细文档

完整架构说明见 **[src/inspection_bringup/README.md](src/inspection_bringup/README.md)**，包含：

- 消息接口契约（字段/单位/枚举约定）
- 节点详解与实现指南
- 状态机、导航配置说明
- 「如何新增一个感知任务」的扩展指南
- 桩函数实现清单

## 开发环境

- ROS 2 Lyrical（注意：`ament_target_dependencies` 已移除，消息包用 `rosidl_generate_interfaces`）
- 构建需安装 `slam_toolbox`、`nav2`（可选，未安装时感知与状态机仍可运行）

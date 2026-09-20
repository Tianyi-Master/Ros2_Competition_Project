# 巡检机器人（Inspection Robot）代码架构

基于 **YOLO + OpenCV + Nav2** 的 ROS 2（**Lyrical** / Ubuntu 26.04）巡检机器人代码架构。

> 当前为**架构骨架（stub）**：节点可启动、消息类型齐全、数据流通路完整；
> 推理与业务逻辑以 `TODO` 形式留待实现。本文件是完整架构文档。

---

## 目录

1. [功能清单](#1-功能清单)
2. [包结构](#2-包结构)
3. [架构分层与数据流](#3-架构分层与数据流)
4. [消息接口契约](#4-消息接口契约)
5. [节点详解](#5-节点详解)
6. [任务状态机](#6-任务状态机)
7. [导航（SLAM / AMCL / 泊车）](#7-导航slam--amcl--泊车)
8. [传感器话题与坐标系](#8-传感器话题与坐标系)
9. [构建与启动](#9-构建与启动)
10. [如何新增一个感知任务](#10-如何新增一个感知任务)
11. [开发约定](#11-开发约定)
12. [实现桩函数清单](#12-实现桩函数清单)

---

## 1. 功能清单

| # | 功能 | 节点（`ros2 run` 可执行名） | 输出话题 | 消息类型 |
|---|---|---|---|---|
| 1 | 红绿灯识别 | `traffic_light` | `/perception/traffic_light` | `TrafficLight` |
| 2 | 人群数量 | `crowd` | `/perception/crowd` | `CrowdCount` |
| 3 | 垃圾桶满/未满 | `bin_status` | `/perception/bin_status` | `BinStatus` |
| 4 | 楼宇火灾(烟/光) | `fire` | `/perception/fire` | `FireEvent` |
| 5 | 车辆车牌 | `license_plate` | `/perception/license_plate` | `LicensePlate` |
| 6 | 异常温度 | `temperature` | `/perception/temperature` | `TemperatureReading` |
| 7 | 站房仪表读取 | `meter` | `/perception/meter` | `MeterReading` |
| 8 | 电动车状态(倒伏/违停) | `ev_status` | `/perception/ev_status` | `EVStatus` |
| — | 统一告警 | （各感知节点） | `/perception/alert` | `InspectionAlert` |
| 9 | 巡检状态机 | `mission_server` | `/mission/state` | `std_msgs/String` |
| 10 | 定义位置泊车 | `parking_controller` | Nav2 action | `NavigateToPose`/`FollowWaypoints` |
| 11 | 激光 SLAM | `slam_toolbox`（`slam.launch.py`） | `/map` | `nav_msgs/OccupancyGrid` |
| 12 | AMCL 定位 | `nav2_amcl`（`amcl.launch.py`） | `/amcl_pose` | `PoseWithCovarianceStamped` |

> 注意：**可执行名 ≠ 节点名**。`ros2 run perception traffic_light` 启动的是
> 可执行 `traffic_light`，其内部节点名为 `traffic_light_node`。

---

## 2. 包结构

```
~/ros2_ws/src/
├── inspection_interfaces/          # 自定义消息接口（ament_cmake / rosidl）
│   ├── msg/                        # 12 个消息定义（见 §4）
│   ├── CMakeLists.txt
│   └── package.xml
│
├── perception/                     # 感知节点，单包多节点（ament_python）
│   ├── perception/
│   │   ├── base/
│   │   │   ├── vision_node.py      # VisionNode 基类（订阅→转换→推理→发布）
│   │   │   ├── detector.py         # YoloDetector（模型后端隔离层，惰性加载）
│   │   │   └── utils.py            # bbox 构造与坐标转换
│   │   ├── nodes/                  # 8 个任务节点，各自只实现 run_inference()
│   │   │   ├── traffic_light_node.py
│   │   │   ├── crowd_node.py
│   │   │   ├── bin_status_node.py
│   │   │   ├── fire_node.py
│   │   │   ├── license_plate_node.py
│   │   │   ├── temperature_node.py
│   │   │   ├── meter_node.py
│   │   │   └── ev_status_node.py
│   │   └── config/
│   │       ├── models.yaml         # 各任务模型路径/阈值/类别
│   │       └── topics.yaml         # 话题命名约定
│   └── setup.py                    # 注册 8 个 console_scripts
│
├── mission_controller/             # 任务编排 + 泊车（ament_python）
│   ├── mission_controller/
│   │   ├── states.py               # 状态常量 + 状态机图
│   │   ├── mission_server.py       # 巡检状态机（订阅感知→驱动状态）
│   │   └── parking.py              # Nav2 泊车动作客户端
│   └── setup.py
│
└── inspection_bringup/             # launch + Nav2 配置（ament_cmake）
    ├── launch/
    │   ├── perception.launch.py    # 启动 8 个感知节点
    │   ├── mission.launch.py       # 状态机 + 泊车
    │   ├── slam.launch.py          # slam_toolbox 建图
    │   ├── amcl.launch.py          # map_server + AMCL 定位
    │   ├── navigation.launch.py    # Nav2 导航栈
    │   └── inspection_bringup.launch.py  # 总入口
    ├── config/
    │   ├── nav2_params.yaml        # Nav2 参数骨架
    │   ├── mapper_params_online_async.yaml  # slam_toolbox 参数
    │   ├── topics.yaml             # 传感器/导航话题与坐标系约定
    │   └── waypoints.yaml          # 定义泊车点
    └── maps/                       # 地图文件存放
```

---

## 3. 架构分层与数据流

```
┌─────────────────────────────────────────────────────────────┐
│                       感知层 (perception)                     │
│                                                             │
│  RGB相机 /camera/image_raw ─┬─> traffic_light ─> TrafficLight │
│                             ├─> crowd ─────────> CrowdCount  │
│                             ├─> bin_status ────> BinStatus    │
│                             ├─> fire ──────────> FireEvent    │
│                             ├─> license_plate ─> LicensePlate │
│                             ├─> meter ─────────> MeterReading │
│                             └─> ev_status ─────> EVStatus     │
│  热像仪 /thermal/image_raw ──> temperature ────> TemperatureReading
│                                  │                          │
│                                  └──> /perception/alert (InspectionAlert)
└─────────────────────────────────────────────────────────────┘
                              │ 订阅全部感知结果 + 告警
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  编排层 (mission_controller)                   │
│                                                             │
│  mission_server: 状态机 IDLE→PATROL→INSPECT→ALERT→PARK       │
│                  发布 /mission/state                         │
│  parking_controller: Nav2 泊车（动作客户端）                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      导航层 (Nav2)                            │
│                                                             │
│  激光 /scan ─> slam_toolbox(建图) / amcl(定位)                │
│              └─> /map, /amcl_pose ─> 规划/控制 ─> /cmd_vel     │
└─────────────────────────────────────────────────────────────┘
```

**数据流一句话总结**：传感器（RGB/热像/激光）→ 感知节点 → 感知结果话题 →
状态机 → 驱动 Nav2 导航（巡检 + 泊车）。

---

## 4. 消息接口契约

全部消息位于 `inspection_interfaces/msg/`，字段单位与枚举含义已在各 `.msg`
文件中注释。这里列出关键约定：

### 通用

| 消息 | 字段 | 说明 |
|---|---|---|
| `BoundingBox2D` | x,y,width,height | 中心点+尺寸，像素坐标，原点在图像左上角 |
| `Detection` | class_id, class_name, confidence, bbox | 单目标检测结果 |
| `DetectionArray` | header, detections[] | 一帧全部检测 |

### 任务专用（均含 `std_msgs/Header header`）

| 消息 | 关键字段 | 约定 |
|---|---|---|
| `TrafficLight` | state, confidence | state ∈ {"RED","YELLOW","GREEN","UNKNOWN"} |
| `CrowdCount` | count, density | density 单位 人/m²，未知为 0 |
| `BinStatus` | status, fill_ratio, confidence | status: EMPTY=0/FULL=1/UNKNOWN=2 |
| `FireEvent` | smoke, flame, confidence, bbox | bool 标志烟/火 |
| `LicensePlate` | plate_text, confidence, bbox | 无车牌时 plate_text="" |
| `TemperatureReading` | temperature, threshold, abnormal | 单位 ℃ |
| `MeterReading` | value, unit, abnormal, confidence | 单位如 V/A/MPa |
| `EVStatus` | state, confidence, bbox | UPRIGHT=0/FALLEN=1/ILLEGAL_PARKING=2/UNKNOWN=3 |
| `InspectionAlert` | module, severity, message | severity: INFO=0/WARNING=1/ERROR=2 |

---

## 5. 节点详解

### 5.1 基类 `VisionNode`（perception/base/vision_node.py）

统一处理「订阅图像 → cv_bridge 转 BGR numpy → `run_inference()` → 打时间戳 →
发布结果」。子类只需实现 `run_inference(image)`：

- 返回对应消息 → 基类填充 `header.stamp/frame_id` 后发布；
- 返回 `None` → 基类跳过本帧发布（避免无检测时刷屏）；
- 调用 `self.publish_alert(severity, message)` → 发布 `InspectionAlert`。

公共参数（均可用 launch 覆盖）：`image_topic` / `result_topic` /
`alert_topic` / `model_path` / `confidence_threshold` / `frame_id`。

### 5.2 检测器 `YoloDetector`（perception/base/detector.py）

模型后端隔离层：惰性加载 `ultralytics.YOLO`，`detect()` 返回与后端无关的
`(class_id, class_name, confidence, (x,y,w,h))` 列表。换后端（TensorRT 等）
只需改这一个类。

### 5.3 各任务节点

8 个节点的 `run_inference()` 内已用注释写出分步实现指南（算法思路、
后处理、阈值、告警触发条件），实现时直接照着填即可。

---

## 6. 任务状态机

```
IDLE ──启动──> PATROL ──到达巡检点──> INSPECT
  ^                                    │
  │                                    ├─异常─> ALERT ──处理完──> PATROL
  │                                    │
  └────────返航 / 结束 <───────────────┴─结束──> PARK
```

- `IDLE` 空闲 · `PATROL` 巡逻 · `INSPECT` 巡检 · `ALERT` 告警 · `PARK` 泊车
- 状态机在 `mission_server.py`，订阅全部感知结果 + 告警，各回调的转移规则
  已写 TODO 说明（如「FULL → WARNING 告警」「火灾 → ERROR 告警 + 停靠」）。

---

## 7. 导航（SLAM / AMCL / 泊车）

| 环节 | launch | 说明 |
|---|---|---|
| 建图 | `slam.launch.py` | slam_toolbox 在线异步建图，参数见 `mapper_params_online_async.yaml` |
| 定位 | `amcl.launch.py` | map_server 加载地图 + AMCL 激光定位 |
| 导航 | `navigation.launch.py` | Nav2 完整栈，参数见 `nav2_params.yaml` |
| 泊车 | `parking.py` | `NavigateToPose`（单点）/ `FollowWaypoints`（多点） |

泊车点定义在 `config/waypoints.yaml`，实现 `parking.py` 后从该文件加载。

---

## 8. 传感器话题与坐标系

| 输入话题 | 默认值 | 用途 |
|---|---|---|
| `/camera/image_raw` | RGB 相机 | 7 个视觉任务 |
| `/thermal/image_raw` | 热像仪 | 温度识别 |
| `/scan` | 激光雷达 | SLAM / AMCL / 避障 |
| `/odom` / `/imu` | 里程计 / IMU | 导航 |

坐标系（TF 帧）：`map` ← `odom` ← `base_link` ← 各传感器（`base_footprint`
在 `base_link` 下方）。感知结果的 `frame_id` 默认 `camera_link`（参数可改）。

---

## 9. 构建与启动

```bash
# 1. 构建
cd ~/Ros2_Competition_Project
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
source install/setup.bash

# 2. 仅感知 + 任务编排（无需导航/硬件，节点即可启动）
ros2 launch inspection_bringup inspection_bringup.launch.py

# 3. 建图（需 slam_toolbox + 激光）
ros2 launch inspection_bringup slam.launch.py

# 4. 定位 + 导航（需 Nav2 + 地图文件 maps/map.yaml）
ros2 launch inspection_bringup inspection_bringup.launch.py nav:=true
```

单节点调试示例：

```bash
ros2 run perception traffic_light --ros-args \
  -p image_topic:=/my_camera/image_raw \
  -p result_topic:=/my_result
```

---

## 10. 如何新增一个感知任务

1. 在 `inspection_interfaces/msg/` 定义消息，加入 `CMakeLists.txt` 的
   `rosidl_generate_interfaces` 列表；
2. 在 `perception/perception/nodes/` 新建 `xxx_node.py`，继承 `VisionNode`，
   实现 `run_inference()`；
3. 在 `perception/setup.py` 的 `console_scripts` 注册可执行名；
4. （可选）在 `perception/config/models.yaml` 增加该任务的模型配置；
5. 在 `inspection_bringup/launch/perception.launch.py` 的 `rgb_tasks` 列表加一行；
6. 在 `mission_controller/mission_server.py` 增加订阅与回调。

---

## 11. 开发约定

- **Lyrical 的 CMake 差异**：`ament_target_dependencies()` 已移除。消息包用
  `rosidl_generate_interfaces`（无需手动 `target_link_libraries`）；普通 C++
  库用 `target_link_libraries(target pkg::pkg)` 或 `${pkg_TARGETS}`。
- **CLion**：构建带 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`，在 CLion 打开
  `build/compile_commands.json`，`Tools → Compilation Database → Change Project
  Root` 设为 `~/ros2_ws`。
- **nav2 / slam_toolbox 为可选依赖**：未安装时，感知与状态机可正常运行；
  `parking.py` 会检测 nav2 缺失并降级为禁用状态，导航 launch 文件作为模板
  待装好后使用。

---

## 12. 实现桩函数清单

按依赖顺序推进：

1. 在 `perception/config/models.yaml` 填各任务模型权重路径；
2. 实现 `perception/nodes/*_node.py` 的 `run_inference()`（注释内已给步骤）；
3. 实现 `mission_controller/mission_server.py` 各回调的状态转移规则；
4. 实现 `parking.py` 的 `park_at_pose()` / `park_at_waypoints()`；
5. 安装 `slam_toolbox` + `nav2`，标定 `nav2_params.yaml` 与 `waypoints.yaml`。

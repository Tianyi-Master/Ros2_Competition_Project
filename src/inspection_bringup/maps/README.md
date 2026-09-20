# maps

存放建图产出的地图文件（`.pgm` + `.yaml`）。

建图流程：
1. `ros2 launch inspection_bringup slam.launch.py` 建图
2. 遥控/自动巡场后 `ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/inspection_bringup/maps/map`
3. 之后用 `amcl.launch.py` / `navigation.launch.py` 加载 `map.yaml` 定位导航

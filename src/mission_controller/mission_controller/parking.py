"""定义位置泊车（Nav2 动作客户端，骨架）。

通过 Nav2 的 ``NavigateToPose`` / ``FollowWaypoints`` 动作，驱动机器人
行驶到预定义的泊车点（见 inspection_bringup/config/waypoints.yaml）。

nav2_msgs 未安装时本模块仍可导入（import 被保护），节点会打印警告并禁用
泊车功能，保证 mission_controller 包在无 Nav2 环境下也能运行。
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

try:
    from nav2_msgs.action import FollowWaypoints, NavigateToPose  # noqa: F401
    _NAV2_AVAILABLE = True
except ImportError:
    _NAV2_AVAILABLE = False


class ParkingController(Node):
    """把机器人导航到预定义泊车点。

    两个动作接口：
        - ``NavigateToPose``   ：单点导航（/navigate_to_pose）
        - ``FollowWaypoints``  ：多点顺序导航（/follow_waypoints）
    """

    def __init__(self):
        super().__init__('parking_controller')

        # 泊车点：逗号分隔的 "x,y,yaw" 列表；后续改为从 waypoints.yaml 加载。
        self.declare_parameter('waypoints', '0.0,0.0,0.0')
        self._waypoint_spec = self.get_parameter('waypoints').value

        self._navigate_client = None
        self._follow_client = None

        if _NAV2_AVAILABLE:
            self._navigate_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
            self._follow_client = ActionClient(self, FollowWaypoints, '/follow_waypoints')
            self.get_logger().info('parking controller ready (Nav2 available)')
        else:
            self.get_logger().warning(
                'nav2_msgs not installed; parking actions disabled (stub)')

    def park_at_pose(self, pose):
        """单点泊车：发送 NavigateToPose 目标并等待结果。

        TODO 实现示例::

            goal = NavigateToPose.Goal()
            goal.pose = pose  # PoseStamped
            self._navigate_client.wait_for_server()
            future = self._navigate_client.send_goal_async(goal)
            result = await future  # 或在异步回调中处理
        """
        raise NotImplementedError('park_at_pose() not implemented (stub)')

    def park_at_waypoints(self, waypoints):
        """多点泊车：按顺序经过一组路径点。

        TODO 实现示例::

            goal = FollowWaypoints.Goal()
            goal.poses = [p.pose for p in waypoints]  # list[PoseStamped]
            self._follow_client.wait_for_server()
            future = self._follow_client.send_goal_async(goal)
            result = await future
        """
        raise NotImplementedError('park_at_waypoints() not implemented (stub)')


def main(args=None):
    rclpy.init(args=args)
    node = ParkingController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

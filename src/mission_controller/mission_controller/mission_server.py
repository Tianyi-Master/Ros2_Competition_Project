"""巡检任务状态机（骨架）。

订阅全部感知结果与统一告警，驱动巡检状态机并把当前状态发布到
``/mission/state``。状态定义见 :mod:`mission_controller.states`。

本文件是「编排骨架」：通信链路已接好，状态转移的业务规则留 TODO 待填。
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from inspection_interfaces.msg import (
    TrafficLight,
    CrowdCount,
    BinStatus,
    FireEvent,
    LicensePlate,
    TemperatureReading,
    MeterReading,
    EVStatus,
    InspectionAlert,
)

from mission_controller import states


class MissionServer(Node):
    """巡检任务状态机节点。

    职责：
        - 汇总各感知节点的结果与告警；
        - 根据结果驱动状态机（IDLE/PATROL/INSPECT/ALERT/PARK）；
        - 通过 /mission/state 对外发布当前状态（供 UI / 记录 / 其他节点使用）。
    """

    def __init__(self):
        super().__init__('mission_server')

        # ---- 输入话题参数（默认值与 perception/config/topics.yaml 一致）----
        # 集中声明便于统一改话题名，无需改动下方订阅代码。
        topic_defaults = {
            'alert_topic': '/perception/alert',
            'traffic_light_topic': '/perception/traffic_light',
            'crowd_topic': '/perception/crowd',
            'bin_status_topic': '/perception/bin_status',
            'fire_topic': '/perception/fire',
            'license_plate_topic': '/perception/license_plate',
            'temperature_topic': '/perception/temperature',
            'meter_topic': '/perception/meter',
            'ev_status_topic': '/perception/ev_status',
        }
        for name, default in topic_defaults.items():
            self.declare_parameter(name, default)
        self._topics = {n: self.get_parameter(n).value for n in topic_defaults}

        # ---- 状态 ----
        self.state = states.IDLE
        self.state_pub = self.create_publisher(String, '/mission/state', 10)

        # ---- 订阅全部感知输出 ----
        self.create_subscription(
            InspectionAlert, self._topics['alert_topic'], self._on_alert, 10)
        self.create_subscription(
            TrafficLight, self._topics['traffic_light_topic'], self._on_traffic_light, 10)
        self.create_subscription(
            CrowdCount, self._topics['crowd_topic'], self._on_crowd, 10)
        self.create_subscription(
            BinStatus, self._topics['bin_status_topic'], self._on_bin_status, 10)
        self.create_subscription(
            FireEvent, self._topics['fire_topic'], self._on_fire, 10)
        self.create_subscription(
            LicensePlate, self._topics['license_plate_topic'], self._on_license_plate, 10)
        self.create_subscription(
            TemperatureReading, self._topics['temperature_topic'], self._on_temperature, 10)
        self.create_subscription(
            MeterReading, self._topics['meter_topic'], self._on_meter, 10)
        self.create_subscription(
            EVStatus, self._topics['ev_status_topic'], self._on_ev_status, 10)

        self._publish_state()
        self.get_logger().info('mission server started in state %s' % self.state)

    # ------------------------------------------------------------------
    # 状态机辅助
    # ------------------------------------------------------------------
    def _transition(self, new_state):
        """状态迁移：仅在状态变化时打印日志并发布新状态。"""
        if new_state == self.state:
            return
        self.get_logger().info('state transition: %s -> %s' % (self.state, new_state))
        self.state = new_state
        self._publish_state()

    def _publish_state(self):
        msg = String()
        msg.data = self.state
        self.state_pub.publish(msg)

    # ------------------------------------------------------------------
    # 感知回调（状态转移规则 TODO，按部署需求实现）
    # ------------------------------------------------------------------
    def _on_alert(self, msg):
        # TODO: 收到 ERROR 级告警时迁移到 ALERT；WARNING 级仅记录。
        pass

    def _on_traffic_light(self, msg):
        # TODO: RED 灯时暂停导航（通过 Nav2 取消当前目标），GREEN 恢复。
        pass

    def _on_crowd(self, msg):
        # TODO: 人数/密度超过阈值时减速或绕行，并记录。
        pass

    def _on_bin_status(self, msg):
        # TODO: FULL 时生成 InspectionAlert(WARNING) 并记录巡检点。
        pass

    def _on_fire(self, msg):
        # TODO: smoke/flame 为真时立即 ALERT + ERROR 告警，停靠并上报。
        pass

    def _on_license_plate(self, msg):
        # TODO: 记录车牌，用于门禁/车辆跟踪（写入日志或数据库）。
        pass

    def _on_temperature(self, msg):
        # TODO: abnormal 为真时 ERROR 告警，必要时后撤远离高温点。
        pass

    def _on_meter(self, msg):
        # TODO: abnormal 为真时 WARNING 告警并记录读数。
        pass

    def _on_ev_status(self, msg):
        # TODO: FALLEN / ILLEGAL_PARKING 时 WARNING 告警并记录位置。
        pass


def main(args=None):
    rclpy.init(args=args)
    node = MissionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

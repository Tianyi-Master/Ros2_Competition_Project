"""视觉感知节点基类。

所有「订阅图像 → 推理 → 发布结果」的感知节点都继承 :class:`VisionNode`，
从而复用同一套通信骨架，子类只需实现 :meth:`run_inference` 一个方法。
"""

import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image

from inspection_interfaces.msg import InspectionAlert


class VisionNode(Node):
    """视觉任务节点的公共父类。

    数据流（统一在基类完成）::

        图像话题 --订阅--> _image_callback --cv_bridge 转 numpy--> run_inference()
            --> 打时间戳/坐标系 --> result_pub 发布结果
            （可选）--> publish_alert() --> alert_pub 发布告警

    子类约定：
        - 构造函数调用 ``super().__init__(node_name, result_msg_type,
          default_result_topic, default_image_topic=...)`` 即可；
        - 只实现 :meth:`run_inference(image)`，返回对应结果消息；
        - 返回 ``None`` 表示本帧无结果，基类会跳过发布（避免刷屏）。

    所有话题/模型/阈值均通过 ROS 参数配置，可在 launch 或命令行覆盖，
    无需改代码即可适配不同硬件。
    """

    def __init__(self, node_name, result_msg_type,
                 default_result_topic, default_image_topic='/camera/image_raw'):
        super().__init__(node_name)

        # ---- 参数声明（均可用 launch / --ros-args 覆盖）----
        self.declare_parameter('image_topic', default_image_topic)
        self.declare_parameter('result_topic', default_result_topic)
        self.declare_parameter('alert_topic', '/perception/alert')
        self.declare_parameter('model_path', '')
        self.declare_parameter('confidence_threshold', 0.5)
        self.declare_parameter('frame_id', 'camera_link')

        image_topic = self.get_parameter('image_topic').value
        result_topic = self.get_parameter('result_topic').value
        alert_topic = self.get_parameter('alert_topic').value
        self._frame_id = self.get_parameter('frame_id').value
        self.model_path = self.get_parameter('model_path').value
        self.conf_threshold = self.get_parameter('confidence_threshold').value

        # ---- 通信 ----
        # 图像订阅使用 sensor_data QoS（相机驱动常用配置）。
        # 无相机硬件时订阅只是收不到数据，节点不会崩溃。
        self._bridge = CvBridge()
        self.image_sub = self.create_subscription(
            Image, image_topic, self._image_callback, qos_profile_sensor_data)

        # 结果与告警发布器；result_msg_type 由子类传入，基类无需知道具体类型。
        self.result_pub = self.create_publisher(result_msg_type, result_topic, 10)
        self.alert_pub = self.create_publisher(InspectionAlert, alert_topic, 10)

        self.get_logger().info(
            'Started: subscribing %s -> publishing %s' % (image_topic, result_topic))

    def _image_callback(self, msg):
        """图像回调：转换格式后交给子类推理。

        单帧转换失败只告警并跳过，不抛异常，保证节点在坏帧/不支持编码下持续运行。
        """
        try:
            image = self._bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as exc:  # noqa: BLE001 - 坏帧不应终止节点
            self.get_logger().warning('Failed to convert image: %s' % exc)
            return

        result = self.run_inference(image)
        if result is None:
            return
        # 统一填充时间戳与坐标系，子类无需关心 header。
        result.header.stamp = self.get_clock().now().to_msg()
        result.header.frame_id = self._frame_id
        self.result_pub.publish(result)

    def run_inference(self, image):
        """对一帧 BGR numpy 图像做推理，返回结果消息。

        参数:
            image (np.ndarray): HxWx3 的 BGR 图像（由 cv_bridge 转换而来）。

        返回:
            对应的结果消息（如 TrafficLight / CrowdCount ...）；
            返回 ``None`` 表示本帧不发布。
        """
        raise NotImplementedError

    def publish_alert(self, severity, message, module=None):
        """发布统一告警（供子类在检测到异常时调用）。

        参数:
            severity (int): 告警等级，见 InspectionAlert 的 INFO/WARNING/ERROR 常量。
            message (str): 人类可读描述。
            module (str | None): 来源模块名，缺省用节点名。
        """
        alert = InspectionAlert()
        alert.header.stamp = self.get_clock().now().to_msg()
        alert.header.frame_id = self._frame_id
        alert.module = module if module else self.get_name()
        alert.severity = severity
        alert.message = message
        self.alert_pub.publish(alert)

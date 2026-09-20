"""异常温度识别节点。

从热像仪图像读取温度，超过阈值即判定异常，发布
``inspection_interfaces/msg/TemperatureReading``。
该节点输入是热像话题（非 RGB），由 ``image_topic`` 参数区分。
"""

import rclpy

from perception.base.vision_node import VisionNode
from inspection_interfaces.msg import TemperatureReading, InspectionAlert


class TemperatureNode(VisionNode):
    """读取温度并标记异常。

    输出话题: /perception/temperature (TemperatureReading)
    告警话题: /perception/alert (InspectionAlert)
    输入话题: 默认 /thermal/image_raw（热像仪，非 RGB 相机）
    参数: threshold_celsius（报警阈值，默认 60.0℃）
    """

    def __init__(self):
        super().__init__(
            node_name='temperature_node',
            result_msg_type=TemperatureReading,
            default_result_topic='/perception/temperature',
            default_image_topic='/thermal/image_raw',
        )
        # 该节点专属参数：温度报警阈值。
        self.declare_parameter('threshold_celsius', 60.0)
        self._threshold = self.get_parameter('threshold_celsius').value

    def run_inference(self, image):
        # TODO 实现步骤：
        #   1. 热像图一般是 16-bit 单通道，需先按传感器标定把像素灰度映射到
        #      摄氏温度（不同热像仪映射公式不同）；
        #   2. 取感兴趣区域（或全图）的最高温度写入 temperature；
        #   3. abnormal = temperature >= self._threshold；为 True 时调用
        #      self.publish_alert(InspectionAlert.ERROR, 'temperature abnormal')。
        msg = TemperatureReading()
        msg.temperature = 0.0
        msg.threshold = self._threshold
        msg.abnormal = False
        self.get_logger().debug('temperature inference not implemented (stub)')
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

"""红绿灯识别节点。

从 RGB 相机图像识别红绿灯的灯色（红/黄/绿），发布
``inspection_interfaces/msg/TrafficLight``。
"""

import rclpy

from perception.base.vision_node import VisionNode
from inspection_interfaces.msg import TrafficLight


class TrafficLightNode(VisionNode):
    """识别红绿灯灯色状态。

    输出话题: /perception/traffic_light (TrafficLight)
    输入话题: 由 image_topic 参数决定，默认 /camera/image_raw
    """

    def __init__(self):
        super().__init__(
            node_name='traffic_light_node',
            result_msg_type=TrafficLight,
            default_result_topic='/perception/traffic_light',
        )

    def run_inference(self, image):
        # TODO 实现步骤：
        #   1. 用 YoloDetector（模型类别 red/yellow/green）检测图像中的红绿灯；
        #   2. 取置信度最高且 >= self.conf_threshold 的检测框；
        #   3. 按 class_name 映射到 state："red"->RED、"yellow"->YELLOW、
        #      "green"->GREEN，并把置信度写入 confidence；
        #   4. 帧内无红绿灯时返回 None（基类会跳过发布）。
        msg = TrafficLight()
        msg.state = 'UNKNOWN'
        msg.confidence = 0.0
        self.get_logger().debug('traffic light inference not implemented (stub)')
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = TrafficLightNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

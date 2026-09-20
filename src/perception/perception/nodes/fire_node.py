"""楼宇火灾（烟/光）识别节点。

检测画面中的烟雾与火光，发布 ``inspection_interfaces/msg/FireEvent``。
火灾属于高危事件，检测到后应同时调用 ``publish_alert(ERROR, ...)``。
"""

import rclpy

from perception.base.vision_node import VisionNode
from perception.base.utils import make_bbox
from inspection_interfaces.msg import FireEvent, InspectionAlert


class FireNode(VisionNode):
    """检测烟雾 / 火光。

    输出话题: /perception/fire (FireEvent)
    告警话题: /perception/alert (InspectionAlert)
    输入话题: 默认 /camera/image_raw
    """

    def __init__(self):
        super().__init__(
            node_name='fire_node',
            result_msg_type=FireEvent,
            default_result_topic='/perception/fire',
        )

    def run_inference(self, image):
        # TODO 实现步骤：
        #   1. 用 YoloDetector（类别 smoke / flame）检测；
        #   2. 分别取 smoke、flame 两类中置信度最高者，>= self.conf_threshold
        #      时置对应布尔为 True，并把最高置信度与框写入 confidence / bbox；
        #   3. 若检测到 smoke 或 flame，调用
        #      self.publish_alert(InspectionAlert.ERROR, 'fire detected')；
        #   4. 帧内无烟无火时返回 None。
        msg = FireEvent()
        msg.smoke = False
        msg.flame = False
        msg.confidence = 0.0
        msg.bbox = make_bbox(0.0, 0.0, 0.0, 0.0)
        self.get_logger().debug('fire inference not implemented (stub)')
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = FireNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

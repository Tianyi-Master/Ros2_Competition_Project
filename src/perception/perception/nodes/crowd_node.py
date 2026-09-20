"""人群数量识别节点。

统计 RGB 图像中的人数（可扩展为人群密度），发布
``inspection_interfaces/msg/CrowdCount``。
"""

import rclpy

from perception.base.vision_node import VisionNode
from inspection_interfaces.msg import CrowdCount


class CrowdNode(VisionNode):
    """统计画面内人数。

    输出话题: /perception/crowd (CrowdCount)
    输入话题: 默认 /camera/image_raw
    """

    def __init__(self):
        super().__init__(
            node_name='crowd_node',
            result_msg_type=CrowdCount,
            default_result_topic='/perception/crowd',
        )

    def run_inference(self, image):
        # TODO 实现步骤：
        #   1. 用 YoloDetector（类别 person）检测人体框；
        #   2. count = 置信度 >= self.conf_threshold 的人数；
        #   3. density 可选：若已知监控区域面积，用 count/面积 计算人/m^2，
        #      面积未知时保持 0.0。
        msg = CrowdCount()
        msg.count = 0
        msg.density = 0.0
        self.get_logger().debug('crowd count inference not implemented (stub)')
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = CrowdNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

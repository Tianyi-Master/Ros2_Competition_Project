"""垃圾桶满/未满状态识别节点。

对垃圾桶做「满 / 未满」二分类，估算装满比例，发布
``inspection_interfaces/msg/BinStatus``。
"""

import rclpy

from perception.base.vision_node import VisionNode
from inspection_interfaces.msg import BinStatus


class BinStatusNode(VisionNode):
    """判断垃圾桶是否已满。

    输出话题: /perception/bin_status (BinStatus)
    输入话题: 默认 /camera/image_raw
    """

    def __init__(self):
        super().__init__(
            node_name='bin_status_node',
            result_msg_type=BinStatus,
            default_result_topic='/perception/bin_status',
        )

    def run_inference(self, image):
        # TODO 实现步骤：
        #   1. 检测垃圾桶（类别 trash_bin_empty / trash_bin_full）；
        #   2. 取置信度最高且 >= self.conf_threshold 的框：
        #        trash_bin_full -> status=FULL，trash_bin_empty -> status=EMPTY；
        #   3. fill_ratio 可用「垃圾在桶内高度占比」回归得到（简单起见：FULL=1.0、
        #      EMPTY=0.0，或用框内分割掩码占比估算）；
        #   4. 帧内无垃圾桶时返回 None。
        msg = BinStatus()
        msg.status = BinStatus.UNKNOWN
        msg.fill_ratio = 0.0
        msg.confidence = 0.0
        self.get_logger().debug('bin status inference not implemented (stub)')
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = BinStatusNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

"""电动车状态（倒伏/违停）识别节点。

对电动车分类：正常停放 / 倒伏 / 违停，发布
``inspection_interfaces/msg/EVStatus``。
"""

import rclpy

from perception.base.vision_node import VisionNode
from perception.base.utils import make_bbox
from inspection_interfaces.msg import EVStatus


class EVStatusNode(VisionNode):
    """分类电动车状态。

    输出话题: /perception/ev_status (EVStatus)
    输入话题: 默认 /camera/image_raw
    """

    def __init__(self):
        super().__init__(
            node_name='ev_status_node',
            result_msg_type=EVStatus,
            default_result_topic='/perception/ev_status',
        )

    def run_inference(self, image):
        # TODO 实现步骤：
        #   1. 用 YoloDetector 检测电动车（类别 ev_upright / ev_fallen /
        #      ev_illegal_parking）；
        #   2. 取置信度最高且 >= self.conf_threshold 的框，按类别映射 state：
        #      ev_upright->UPRIGHT、ev_fallen->FALLEN、
        #      ev_illegal_parking->ILLEGAL_PARKING；
        #   3. 写入 confidence 与 bbox；
        #   4. 帧内无电动车时返回 None。
        msg = EVStatus()
        msg.state = EVStatus.UNKNOWN
        msg.confidence = 0.0
        msg.bbox = make_bbox(0.0, 0.0, 0.0, 0.0)
        self.get_logger().debug('ev status inference not implemented (stub)')
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = EVStatusNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

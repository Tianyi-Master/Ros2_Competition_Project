"""车辆车牌识别节点。

先定位车牌区域，再对车牌字符做 OCR，发布
``inspection_interfaces/msg/LicensePlate``。
"""

import rclpy

from perception.base.vision_node import VisionNode
from perception.base.utils import make_bbox
from inspection_interfaces.msg import LicensePlate


class LicensePlateNode(VisionNode):
    """检测车牌并识别字符。

    输出话题: /perception/license_plate (LicensePlate)
    输入话题: 默认 /camera/image_raw

    识别分两段：检测（YOLO 定位车牌框）+ OCR（如 EasyOCR / PaddleOCR）。
    """

    def __init__(self):
        super().__init__(
            node_name='license_plate_node',
            result_msg_type=LicensePlate,
            default_result_topic='/perception/license_plate',
        )

    def run_inference(self, image):
        # TODO 实现步骤：
        #   1. 用 YoloDetector（类别 license_plate）定位车牌框；
        #   2. 裁剪车牌区域，做矫正/二值化后交给 OCR 识别字符；
        #   3. 把 OCR 文本写入 plate_text，识别置信度写入 confidence，
        #      车牌框写入 bbox；
        #   4. 帧内无车牌时返回 None。
        msg = LicensePlate()
        msg.plate_text = ''
        msg.confidence = 0.0
        msg.bbox = make_bbox(0.0, 0.0, 0.0, 0.0)
        self.get_logger().debug('license plate inference not implemented (stub)')
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = LicensePlateNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

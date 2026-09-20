"""站房仪表读取节点。

读取指针表 / 数显表的读数，发布 ``inspection_interfaces/msg/MeterReading``。
指针表需要检测指针角度换算数值；数显表则用 OCR。
"""

import rclpy

from perception.base.vision_node import VisionNode
from inspection_interfaces.msg import MeterReading


class MeterNode(VisionNode):
    """读取仪表数值。

    输出话题: /perception/meter (MeterReading)
    输入话题: 默认 /camera/image_raw
    """

    def __init__(self):
        super().__init__(
            node_name='meter_node',
            result_msg_type=MeterReading,
            default_result_topic='/perception/meter',
        )

    def run_inference(self, image):
        # TODO 实现步骤：
        #   1. 检测/定位仪表盘区域（YOLO 类别 meter / gauge）；
        #   2. 指针表：检测指针，用指针角度 + 量程刻度换算 value；
        #      数显表：对显示区域 OCR 得到 value；
        #   3. 填写 unit（如 "V"/"A"/"MPa"）与 confidence；
        #   4. abnormal = value 超出正常量程（正常范围可从参数配置）；
        #   5. 帧内无仪表时返回 None。
        msg = MeterReading()
        msg.value = 0.0
        msg.unit = ''
        msg.abnormal = False
        msg.confidence = 0.0
        self.get_logger().debug('meter reading inference not implemented (stub)')
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = MeterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

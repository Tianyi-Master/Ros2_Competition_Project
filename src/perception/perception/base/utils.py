"""感知节点共用的轻量工具函数。

主要是边界框构造与坐标格式转换，避免在各节点里重复手写。
"""

from inspection_interfaces.msg import BoundingBox2D


def make_bbox(x, y, width, height):
    """用「中心点 + 尺寸」构造 :class:`BoundingBox2D`。

    参数为像素坐标，见 BoundingBox2D.msg 的约定。
    """
    bbox = BoundingBox2D()
    bbox.x = float(x)
    bbox.y = float(y)
    bbox.width = float(width)
    bbox.height = float(height)
    return bbox


def xyxy_to_bbox(x1, y1, x2, y2):
    """把 YOLO 的 xyxy（左上/右下角）转成中心+尺寸的 :class:`BoundingBox2D`。

    很多检测后端直接输出 (x1, y1, x2, y2)，本函数完成到本工程消息格式的转换。
    """
    return make_bbox((x1 + x2) / 2.0, (y1 + y2) / 2.0, x2 - x1, y2 - y1)

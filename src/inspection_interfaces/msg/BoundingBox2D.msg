# 2D 边界框：中心点 (x, y) + 尺寸 (width, height)。
#
# 约定：
#   - 坐标原点为图像左上角，x 向右、y 向下。
#   - 单位均为像素 (pixel)。
#
# 与 YOLO 的 xywh 输出一致；若拿到 xyxy（左上/右下角）格式，
# 用 perception.base.utils.xyxy_to_bbox() 转换。
float32 x        # 框中心 x 坐标
float32 y        # 框中心 y 坐标
float32 width    # 框宽度
float32 height   # 框高度

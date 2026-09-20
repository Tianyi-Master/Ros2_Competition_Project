# 楼宇火灾事件（烟 / 光）。
std_msgs/Header header

bool smoke          # true = 检测到烟雾
bool flame          # true = 检测到火光 / 明火
float32 confidence  # 置信度，取值范围 [0.0, 1.0]
BoundingBox2D bbox  # 火灾区域框；无检测时各字段为 0

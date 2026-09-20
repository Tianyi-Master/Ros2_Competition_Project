# 车辆车牌识别结果。
std_msgs/Header header

string plate_text   # 识别出的车牌字符；未识别到为空字符串 ""
float32 confidence  # 置信度，取值范围 [0.0, 1.0]
BoundingBox2D bbox  # 车牌区域框；无检测时各字段为 0

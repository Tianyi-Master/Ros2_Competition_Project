# 红绿灯识别结果。
std_msgs/Header header

# 灯色状态，取值约定（字符串）：
#   "RED"     红灯
#   "YELLOW"  黄灯
#   "GREEN"   绿灯
#   "UNKNOWN" 未识别到红绿灯 / 无法判断（默认值）
string state

float32 confidence   # 置信度，取值范围 [0.0, 1.0]

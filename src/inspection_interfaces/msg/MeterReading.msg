# 站房仪表（指针表 / 数显表）读数。
std_msgs/Header header

float32 value       # 读取到的仪表数值
string unit         # 单位，如 "V" / "A" / "MPa" / "℃"；未知时为空字符串
bool abnormal       # true = 数值超出正常范围（异常）
float32 confidence  # 置信度，取值范围 [0.0, 1.0]

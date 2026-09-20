# 温度读数（来自热像仪 / 温度传感器）。
std_msgs/Header header

float32 temperature # 温度值，单位：摄氏度 (℃)
float32 threshold   # 报警阈值，单位：℃；由节点参数 threshold_celsius 决定
bool abnormal       # true = 温度超过阈值（异常）

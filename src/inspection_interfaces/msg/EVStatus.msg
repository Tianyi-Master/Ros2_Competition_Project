# 电动车状态（倒伏 / 违停）。
std_msgs/Header header

uint8 UPRIGHT=0           # 正常停放
uint8 FALLEN=1            # 倒伏
uint8 ILLEGAL_PARKING=2   # 违停
uint8 UNKNOWN=3           # 未知 / 未识别到

uint8 state         # 取值：UPRIGHT / FALLEN / ILLEGAL_PARKING / UNKNOWN
float32 confidence  # 置信度，取值范围 [0.0, 1.0]
BoundingBox2D bbox  # 电动车区域框；无检测时各字段为 0

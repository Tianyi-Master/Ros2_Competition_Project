# 垃圾桶满/未满状态。
std_msgs/Header header

uint8 EMPTY=0      # 未满
uint8 FULL=1       # 已满
uint8 UNKNOWN=2    # 未知 / 未识别到

uint8 status        # 取值：EMPTY / FULL / UNKNOWN
float32 fill_ratio  # 装满比例 [0.0, 1.0]，0=空、1=满，未知时 0.0
float32 confidence  # 置信度，取值范围 [0.0, 1.0]

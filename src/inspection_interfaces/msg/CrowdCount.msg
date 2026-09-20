# 人群数量识别结果。
std_msgs/Header header

int32 count       # 检测到的人数（>= 0）
float32 density   # 人群密度，单位：人/平方米；场景面积未知时填 0.0

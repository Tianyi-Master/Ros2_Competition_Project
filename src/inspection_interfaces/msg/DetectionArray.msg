# 一帧图像的全部检测结果（通用透出）。
std_msgs/Header header      # 时间戳 + 相机坐标系
Detection[] detections      # 检测列表（可为空数组，表示本帧无检测）

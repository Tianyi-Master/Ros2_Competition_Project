# 单个目标检测结果（通用类型，供需要原样透出检测框的模块使用）。
int32 class_id          # 类别 ID（对应模型输出的类别索引，-1 表示未知）
string class_name       # 类别名称，如 "person" / "flame" / "license_plate"
float32 confidence      # 置信度，取值范围 [0.0, 1.0]
BoundingBox2D bbox      # 检测框（像素坐标）

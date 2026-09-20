"""YOLO 检测器封装（骨架）。

把模型后端（ultralytics / OpenCV DNN / TensorRT ...）隔离在单一类里，
节点只调用 :meth:`detect` 拿到归一化后的检测结果，换后端无需改动节点代码。
"""


class YoloDetector:
    """惰性加载的 YOLO 检测器包装。

    设计要点：
        - 惰性加载：首次调用 detect 时才导入并实例化模型，避免无模型环境
          下导入 ultralytics 直接报错；
        - 统一输出：detect 返回与后端无关的 ``(class_id, class_name,
          confidence, (x, y, w, h))`` 元组列表，xywh 为像素坐标中心+尺寸。

    TODO: 拿到模型权重后补全 :meth:`_ensure_loaded` 与 :meth:`detect`。
    """

    def __init__(self, model_path, confidence_threshold=0.5, classes=None):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        # 只关心这些类别（可选），为空表示不过滤。
        self.classes = list(classes) if classes else []
        self._model = None

    def _ensure_loaded(self):
        """首次使用时加载模型（幂等）。

        TODO 实现示例::

            from ultralytics import YOLO
            self._model = YOLO(self.model_path)
        """
        if self._model is not None:
            return
        raise NotImplementedError('YoloDetector._ensure_loaded() not implemented (stub)')

    def detect(self, image):
        """对一帧 BGR 图像做推理。

        参数:
            image (np.ndarray): HxWx3 BGR 图像。

        返回:
            list[tuple]: ``(class_id, class_name, confidence, (x, y, w, h))``，
            xywh 为像素坐标；空列表表示无检测。

        TODO 实现示例::

            self._ensure_loaded()
            results = self._model(image, conf=self.confidence_threshold)
            out = []
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    name = r.names[cls_id]
                    if self.classes and name not in self.classes:
                        continue
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    out.append((cls_id, name, float(box.conf[0]),
                                ((x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1)))
            return out
        """
        raise NotImplementedError('YoloDetector.detect() not implemented (stub)')

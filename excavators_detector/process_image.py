import os
import io
import cv2

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

from excavators_detector.yolo import YOLOv8

PATH_TO_MODEL = os.getcwd() + r'\excavators_detector\neuro_models\best.onnx'


def process(bytes):
    image = Image.open(io.BytesIO(bytes)).convert("RGB")
    image = np.array(image)
    image = image[:, :, ::-1].copy()
    yolo = YOLOv8(PATH_TO_MODEL, conf_thres=0.7, iou_thres=0.5)
    yolo(image)
    # rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # detect = yolo.draw_detections(rgb_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if len(yolo.scores) != 0:
        scores_list = yolo.scores.tolist()
        boxes_list = yolo.boxes.tolist()
        class_ids_list = yolo.class_ids.tolist()
        with open(r'C:\Users\konstantin.borovik\Desktop\output.txt', 'w') as f:
            f.write(str(boxes_list))
        for boxes in boxes_list:
            image = cv2.rectangle(
                img=image,
                pt1=(int(boxes[0]), int(boxes[1])),
                pt2=(int(boxes[2]), int(boxes[3])),
                color=(255, 0, 0),
                thickness=2
            )
    return image
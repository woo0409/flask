import cv2
import datetime
import numpy as np
import time

from utils.operation import YOLO


def PutTime(frame):
    """
    在画面帧左上角实时显示时间
    :param frame: 输入帧
    :return: 输出帧
    """
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, current_time, (10, 50), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    return frame


def label(det_obj, frame):
    """
    解析模型检测后的数据并在图像中框出目标物及保存视频等操作
    :param det_obj:模型检测返回的数据
    :param frame: 输入帧
    :return: 输出帧
    """
    is_fall = False

    for i in range(len(det_obj)):
        TypeName = det_obj[i]['classes']

        # 检测到目标
        if TypeName == 'fall':

            # 对视频帧进行标注目标框
            p1 = (det_obj[i]['crop'][0:2])
            p2 = (det_obj[i]['crop'][2:4])
            frame = cv2.rectangle(frame, p1, p2, (0, 255, 0), 3)
            frame = cv2.putText(frame, TypeName, p1, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 120, 0), 3)
            is_fall = True

    return frame, is_fall


def detect(frame, onnx_path="data/model/best.onnx"):
    """
    检测目标，返回目标所在坐标如：[{'crop': [57, 390, 207, 882], 'classes': 'person'},...]
    :param frame:输入帧
    :param onnx_path: 用于检测的模型
    :return:输出帧
    """
    # 镜像转换
    frame = cv2.flip(frame, 1)

    # 实时显示时间
    frame = PutTime(frame)

    # 加载yolov5模型
    frame = np.array(frame)
    yolo = YOLO(onnx_path=onnx_path)
    det_obj = yolo.decect(frame, video=True)

    # 检测视频并标注及后续操作
    frame, is_fall = label(det_obj, frame)

    return frame, is_fall


if __name__ == '__main__':
    print("开始录制")
    time.sleep(5)
    print("结束录制")

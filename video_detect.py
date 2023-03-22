from flask import Flask, Response
import cv2
import time

from utils.process import detect

app = Flask(__name__)


def generate_frames(sava_video=False):
    cap = cv2.VideoCapture(0)
    save_path, recording, out, start_time, fourcc, fps, width, height = None, None, None, None, None, None, None, None

    if sava_video:
        # 初始化需要的参数
        save_path = "runs/video/"
        recording = False

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out_filename = 'output_{}.mp4v'.format(time.strftime('%Y%m%d_%H%M%S'))

        out = cv2.VideoWriter(save_path + out_filename, fourcc, 10, (width, height))

    while True:
        # 逐帧捕获视频
        success, frame = cap.read()
        if not success:
            break

        # 检测视频帧
        frame, is_fall = detect(frame)

        if sava_video:
            if is_fall and not recording:
                print("开始录制!")
                recording = True
                start_time = time.time()

            if recording and time.time() - start_time > 4:
                recording = False
                out.release()
                print("结束录制")

                # 重新新建一个视频存储对象
                out_filename = 'output_{}.mp4v'.format(time.strftime('%Y%m%d_%H%M%S'))
                out = cv2.VideoWriter(save_path + out_filename, fourcc, 10, (width, height))

            # 如果正在录制视频，写入视频帧
            if recording:
                # print("录制中....")
                out.write(frame)

        # 将帧转换为JPG格式
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 生成视频帧
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


@app.route('/video_feed')
def video_feed():
    # 返回视频流响应
    return Response(generate_frames(sava_video=True), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # 将应用程序绑定到本地主机上的IP地址为127.0.0.1，端口号为5000
    app.run(debug=True, host='192.168.31.96', port=5000)

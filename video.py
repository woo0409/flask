from flask import Flask, Response
import cv2
from process import detect

app = Flask(__name__)


def generate_frames(sava_video=False):
    cap = cv2.VideoCapture(0)
    out = None
    while True:
        # 逐帧捕获视频
        success, frame = cap.read()
        if not success:
            break

        if sava_video:
            # 生成用户保存视频的实例
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.mp4v', fourcc, 20, (width, height))

            frame = detect(frame, out)
        else:
            # 检测视频帧
            frame = detect(frame)
        # 将帧转换为JPG格式
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 生成视频帧
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    out.release()


@app.route('/video_feed')
def video_feed():
    # 返回视频流响应
    return Response(generate_frames(sava_video=False), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # 将应用程序绑定到本地主机上的IP地址为127.0.0.1，端口号为5000
    app.run(debug=True, host='192.168.31.96', port=5000)

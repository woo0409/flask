from flask import Flask, Response
import cv2
import time
import os
import paramiko

from utils.process import detect

app = Flask(__name__)


def generate_frames(sava_video=False, limit_time=5):
    cap = cv2.VideoCapture("data/media/test.mp4")
    is_fall, sftp, ssh, out_filename, save_path, recording, out, start_time, fourcc, fps, width, height = \
        False, None, None, None, None, None, None, None, None, None, None, None

    if sava_video:
        # 初始化需要的参数
        save_path = "runs/video/"
        recording = False

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out_filename = 'output_{}.mp4v'.format(time.strftime('%Y%m%d_%H%M%S'))

        out = cv2.VideoWriter(save_path + out_filename, fourcc, fps, (width, height))

        # 建立SFTP连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("150.158.88.159", username="ubuntu", password="5921wjy!")

        # 创建SFTP客户端
        sftp = ssh.open_sftp()

    while True:
        # 逐帧捕获视频
        success, frame = cap.read()
        if not success:
            break

        # 检测视频帧
        frame, is_fall = detect(frame)

        if sava_video:

            if is_fall and not recording:
                start_time = time.time()
                print(f"{start_time}开始录制!")
                recording = True

            if recording and not is_fall:
                end_time = time.time()
                print(f"{end_time}结束录制")
                recording = False
                if end_time - start_time < limit_time:
                    print(f"此次跌倒持续时间长为{end_time-start_time}小于{limit_time},不得已保存")
                    os.remove(save_path+out_filename)
                else:
                    out.release()
                    print("符合要求保存视频")
                #     # 像服务器发送请求
                #     # sftp.put(save_path + out_filename, "/var/www/html/videos/" + out_filename)
                #     # 关闭SFTP连接和SSH会话
                #     # sftp.close()
                #     # ssh.close()

                # 重新新建一个视频存储对象
                out_filename = 'output_{}.mp4v'.format(time.strftime('%Y%m%d_%H%M%S'))
                out = cv2.VideoWriter(save_path + out_filename, fourcc, fps, (width, height))

            # 如果正在录制视频，写入视频帧
            if recording:
                # print("录制中....")
                out.write(frame)

            # if recording and time.time() - start_time > 4:
            #     recording = False
            #     out.release()
            #     print("结束录制")
            #
            #     # 像服务器发送请求
            #     # sftp.put(save_path + out_filename, "/var/www/html/videos/" + out_filename)
            #     # 关闭SFTP连接和SSH会话
            #     # sftp.close()
            #     # ssh.close()
            #
            #     print(f"The file {out_filename} has been saved to /var/www/html/videos/")
            #
            #     # 重新新建一个视频存储对象
            #     out_filename = 'output_{}.mp4v'.format(time.strftime('%Y%m%d_%H%M%S'))
            #     out = cv2.VideoWriter(save_path + out_filename, fourcc, fps, (width, height))

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
    app.run(debug=True, host='192.168.31.97', port=5000)

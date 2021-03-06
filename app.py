#!/usr/bin/env python
from flask import Flask, render_template, Response
from flask_bootstrap import Bootstrap
# 从flask_bootstrap 命名空间中导入

# 使用本地图片进行调试
from camera import Camera
# 使用网络摄像头
# from webCamera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
bootstrap = Bootstrap(app)
# 然后把程序实例传入构造方法进行初始化。
@app.route('/')
def index():
    """返回主页"""
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    '''动态路由部分'''
    return render_template('user.html',name=name)

@app.route('/video')
def video():
    return render_template('video.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# 在网页模板中使用 <img src="{{ url_for('video_feed') }}"> 标签
# 对函数进行调用
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0', debug=True, threaded=True)

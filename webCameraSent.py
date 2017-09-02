import socket
import cv2

cam = cv2.VideoCapture(0)
# 打开电脑的0号摄像头，其他摄像头使用其他编号
# 这里也可以使用本地的视频文件
clisocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# 使用socket进行传输
while cam.isOpened(): 
    success,image=cam.read() # 读摄像头
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
	# 转为灰度图
    res = cv2.resize(gray,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
	# 为了保证传输效果，采用了灰度图并且将图片缩小了进行传输
    ret, jpeg=cv2.imencode('.jpg', res)
	# 因为opencv读取的图片并非jpeg格式，
	# 因此要用motion JPEG模式需要先将图片转码成jpg格式图片
    clisocket.sendto(jpeg.tobytes(),("123.206.196.239",1234))
	# 转化为byte进行发送，发送到服务器地址，以及约定的端口
else:
    cam.release()
    clisocket.close()

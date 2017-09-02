import cv2
import socket
import threading
import time

class Camera(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0) 
        self.svrsocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.svrsocket.bind(("127.0.0.1",1234))
        
    def __del__(self):
        self.video.release()

    def get_frame(self):
        data,address=self.svrsocket.recvfrom(80000)
        return data
    
    def get_frame0(self):
        success, image = self.video.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
class Camera000(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()
            #新建线程
            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
    def __init__(self):
        pass
        #self.cap = cv2.VideoCapture(0)
        #ret,frames = self.cap.read()

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame
        #ret,frame = self.cap.read()
        #return frame
    
    def _thread(cls):
        camera = cv2.VideoCapture(0)
        time.sleep(2)
        while camera.isOpened():
            cls.frame = camera.read()
        # if there hasn't been any clients asking for frames in
        # the last 10 seconds stop the thread
            if time.time() - cls.last_access > 10:
                break
        cls.thread = None

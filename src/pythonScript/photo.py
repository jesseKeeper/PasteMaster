from picamera import PiCamera
from time import sleep


camera = PiCamera()

def capture ():
    global camera
    camera.capture('static/image/view.jpg')
    sleep(5)


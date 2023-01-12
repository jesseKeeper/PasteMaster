from picamera import PiCamera
from time import sleep

camera = PiCamera()
# camera.rotation = 180
camera.capture('static/image/view.jpg')

sleep(5)

SystemExit
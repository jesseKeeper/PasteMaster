import camera
import time

filename = 'static/image/camera.jpg'
camera = camera.Camera(filename)
time.sleep(3)
camera.capture()


from picamera2 import Picamera2
import time

time.sleep(3)

picam2 = Picamera2()
picam2.start_and_capture_file("static/image/view.jpg", delay=0, show_preview=False)
picam2.stop()

time.sleep(3)

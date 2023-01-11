from picamera2 import Picamera2
import time

time.sleep(3)

picam2.start_and_capture_file("static/image/view.jpg", delay=0, show_preview=False)

time.sleep(3)

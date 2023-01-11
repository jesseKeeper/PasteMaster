from picamera2 import Picamera2, Preview
import time

time.sleep(3)

picam2 = Picamera2()
picam2.start_and_capture_file("static/image/view.jpg", delay=0, show_preview=False)

# path = "path/to/image.jpg"

# with open(path, 'rb') as f:
#     jpg = f.read()

# Response.ContentType = "image/jpeg"

# Response.WriteBinary(jpg)
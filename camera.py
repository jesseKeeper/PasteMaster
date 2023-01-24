from picamera2 import Picamera2

class Camera:
    def __init__(self, filename):
        self.picam2 = Picamera2()
        self.filename = filename

    def capture (self):
        self.picam2.start_and_capture_file(self.filename, delay=0, show_preview=False)
        self.picam2.stop()
        self.picam2.close()
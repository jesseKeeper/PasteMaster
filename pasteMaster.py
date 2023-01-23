# ttps://flask.palletsprojects.com/en/2.2.x/quickstart/#file-uploads
import json
import printer
import detect
import time

from flask import Flask, render_template, send_file, request
app = Flask(__name__)

printer1 = printer.Printer("/dev/ttyUSB0", 115200, 55, 50)

demoPadRange = [[2, 0, 0], [55, 255, 255]]
demoPCBRange = [[135, 100, 78], [160, 255, 255]]
pixelsPerMilimeter = 27.3315496994
offset = (69.9, 11.2, 0)

detector = detect.Detector(demoPadRange, demoPCBRange, pixelsPerMilimeter, offset)
detections = []

if printer1.camera:
   filename = 'static/image/camera.jpg'
else:
   filename = 'static/image/demoPCB.jpg'

if __name__ == '__main__':
   app.run()

@app.route('/')
def homes():
   return render_template('index.html')

@app.route('/start', methods=['GET'])
def index():
   global detections
   printer1.make_photo()

   time.sleep(1)
   detections = detector.detect(filename, (75, 150, 100), (3280, 2464))
   
   return render_template('start.html')

@app.route('/pcb')
def get_image():
   global filename

   return send_file(filename, mimetype='image/jpg')

@app.route('/array')
def get_array():
   global detections
   dict = {
    "web_detections": detections[1],
    "printer_detections": detections[0]
   }

   detections_json = json.dumps(dict)
   return (detections_json)

@app.route('/run', methods=['POST'])
def run():
   print (request)

@app.errorhandler(404)
def page_not_found(error):
   return render_template('page_not_found.html'), 404

# ttps://flask.palletsprojects.com/en/2.2.x/quickstart/#file-uploads
import json
import printer
import detect
import time
from flask import Flask, render_template, send_file, request
app = Flask(__name__)

printer1 = printer.Printer("/dev/ttyUSB0", 115200, 75, 57)
lastHome = None
#  = time.time()

# filename, used by capture, detect and return of the image
filename = 'static/image/camera.jpg'
# filename = 'static/image/demoPCB.jpg'

demoPadRange = [[2, 0, 0], [55, 255, 255]]
demoPCBRange = [[135, 100, 78], [160, 255, 255]]
pixelsPerMilimeter = 27.3315496994
offset = (55.5, -2, 0)

detector = detect.Detector(demoPadRange, demoPCBRange, pixelsPerMilimeter, offset)
detections = []

def home_printer_command():
   global printer1, lastHome
   print(time.time() - lastHome)
   if lastHome is None:
      printer1.send_command("G28")
      lastHome = time.time()

   elif (time.time() - lastHome) > 5000:
      printer1.send_command("G28")
      lastHome = time.time()

@app.route('/')
def homes():
   return render_template('index.html')

@app.route('/home', methods=['POST'])
def home_printer():
   return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/start', methods=['GET'])
def index():
   return render_template('start.html')

   
@app.route('/photo', methods=['GET'])
def take_photo():
   global detections
   # printer has to be homed --> fail safe for stepper motors disabled
   home_printer_command()
   # printer1.send_command("G28")

   # printer moves to dedicated point for taking picture of pcb
   printer1.move_for_photo()
   # time.sleep(5)

   # Execute photo script
   file = open(r'./src/pythonScript/photo.py', 'r').read()
   exec(file)
   
   print('I am running the algoritmee')
   # run algoritme to detect points on pcb
   detections = detector.detect(filename, (75, 150, 100), (3280, 2464))
   
   # return the start.html that will show to the user
   return render_template('start.html') # runt direct detections 

  
@app.route('/done', methods=['GET'])
def done(): 
   return render_template('done.html')

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
   args = request.get_json()
   printer1.dispense_at_points(args)
   # time.sleep(10)
   
   return json.dumps({'completed':True}), 200, {'ContentType':'application/json'} 

@app.errorhandler(404)
def page_not_found(error):
   return render_template('page_not_found.html'), 404

if __name__ == '__main__':
   app.run(debug=True, port=5000, host='0.0.0.0')

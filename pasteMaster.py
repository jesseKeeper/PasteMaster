# ttps://flask.palletsprojects.com/en/2.2.x/quickstart/#file-uploads
import json
import printer
import detect
import time
import paste
from flask import Flask, render_template, send_file, request
app = Flask(__name__)

# makes connection with USB0 device (Ender 3)
printer1 = printer.Printer("/dev/ttyUSB0", 115200, 75, 57)
lastHome = 1

# filename, used detect and return of the image
filename = 'static/image/camera.jpg'
# filename = 'static/image/demoPCB.jpg'

# detector parameters
demoPadRange = [[2, 0, 0], [55, 255, 255]]
demoPCBRange = [[135, 100, 78], [160, 255, 255]]
pixelsPerMilimeter = 27.3315496994
offset = (54.5, -2, 0)

detector = detect.Detector(demoPadRange, demoPCBRange, pixelsPerMilimeter, offset)
detections = []

# homes printer if the time has not been longer than 60 seconds
def home_printer_command():
   global printer1, lastHome
   print(time.time() - lastHome)
   if (time.time() - lastHome) > 60:
      printer1.send_command("G28")
      lastHome = time.time()

# returns index.html if IP:5000/ is requested
@app.route('/', methods=['GET'])
def render_home ():
   return render_template('index.html')

# returns index.html if IP:5000/start is requested
@app.route('/start', methods=['GET'])
def render_start ():
   return render_template('start.html')

# returns index.html if IP:5000/done is requested
@app.route('/done', methods=['GET'])
def render_done (): 
   return render_template('done.html')


# runs the home_printer_command if IP:5000/home is requested
@app.route('/home', methods=['POST'])
def home_printer ():
   home_printer_command()
   return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# dispenses some paste if IP:5000/paste is requested
@app.route('/paste', methods=['GET'])
def paste_on_spot ():
   paste.dispense(1000)
   paste.disable_stepper()
   return json.dumps({'pasted':True}), 200, {'ContentType':'application/json'} 

# logic to take a photo and analyse the taken picture
@app.route('/photo', methods=['GET'])
def take_analyse_photo ():
   global detections
   # printer has to be homed --> fail safe for stepper motors disabled
   home_printer_command()

   # printer moves to dedicated point for taking picture of pcb
   printer1.move_for_photo()

   # Execute photo script
   file = open(r'./src/pythonScript/photo.py', 'r').read()
   exec(file)
   
   print('I am running the algoritmee')
   # run algoritme to detect points on pcb
   detections = detector.detect(filename, (75, 150, 100), (3280, 2464))
   
   # return the start.html that will show to the user
   return render_template('start.html')

# returns the image that was recently taken if IP:5000/pcb is requested
@app.route('/pcb', methods=['GET'])
def return_image ():
   global filename
   return send_file(filename, mimetype='image/jpg')

# returns the detected pads of the photo that was recently taken if IP:5000/array is requested
@app.route('/array', methods=['GET'])
def return_json ():
   global detections
   dict = {
      "web_detections": detections[1],
      "printer_detections": detections[0]
   }

   return (json.dumps(dict))

# uses the given JSON to move to the pads to dispense
@app.route('/run', methods=['POST'])
def start_dispensing_paste ():
   # JSON made by adding all the corrected pads from user
   args = request.get_json()

   # printer will be moving to the given points to dispense
   printer1.dispense_at_points(args)
   
   return json.dumps({'completed':True}), 200, {'ContentType':'application/json'} 

# returns user to home page if wrong page has been requested
@app.errorhandler(404)
def page_not_found(error):
   return render_template('page_not_found.html'), 404

if __name__ == '__main__':
   app.run(debug=True, port=5000, host='0.0.0.0')
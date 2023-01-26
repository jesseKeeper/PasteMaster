import serial as pyserial
import threading
import time
from picamera2 import Picamera2
import paste

class Printer:
    def __init__(self, port, baudrate, z_save, z_dispense):
        self.port = port
        self.baud = baudrate
        self.z_safe = z_save
        self.z_dispense = z_dispense
        self.status = "ready"

        time.sleep(2)

        self.serial = pyserial.Serial(self.port, self.baud, timeout=0)

    def serial_status(self):
        global status
        serial_data = ""
        while self.serial.inWaiting():
            serial_data = self.serial.readline().decode()
            print(serial_data)
        if serial_data == "ok\n":
            status = "ready"
        return status

    def send_command(self, command, send_sequence=False):
        self.serial.write(str.encode(command + "\r\n"))
        if not send_sequence:  # Block until completed
            self.serial.write(str.encode("M400" + "\r\n"))
            global status
            status = "processing"
            time.sleep(0.5)
            while self.serial_status() == "processing":
                time.sleep(0.5)
            print("Command completed \n\n")

    def move_printer(self, x, y, z, feedrate):
        self.send_command(f"G1 X{x} Y{y} Z{z} F{feedrate}")

# callable functions:
    def dispense_at_points(self, coordinate_list):
        self.move_printer(0, 0, self.z_safe, 10000)
        paste.dispense(500)
        paste.retract(450)
        time.sleep(10)

        for coordinate in coordinate_list:
            self.move_printer(coordinate[0], coordinate[1], self.z_safe, 10000)
            self.move_printer(coordinate[0], coordinate[1], self.z_dispense, 10000)
            paste.dispense(500)
            time.sleep(2)
            self.move_printer(coordinate[0], coordinate[1], self.z_safe, 10000)
            paste.retract(450)
            self.send_command("M114", True)
            
        paste.disable_stepper()

    def move_for_photo(self):
        self.move_printer(0, 0, 100, 500)
        self.move_printer(75, 150, 100, 5000)
        
        time.sleep(2)


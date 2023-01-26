import printer
import time

printer1 = printer.Printer("/dev/ttyUSB0", 115200, 75, 57)
# printer1.dispense_at_points([[150,150],[150,148.5],[150,147],[150,145.5],[150,144],[150,142.5],[150,141],[150,139.5],[150,138]])
time.sleep(5)
printer1.move_printer(150, 150, 57, 10000)
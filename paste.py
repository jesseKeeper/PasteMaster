
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# define variables
chan_list = [17, 27, 22, 23]  # GPIO ports to use

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Set all pins as output
for pin in chan_list:
    print("Setup pins")
    GPIO.setup(pin, GPIO.OUT)

# initialize array for sequence shift
states = [[1, 0, 0, 1],
          [1, 0, 0, 0],
          [1, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 1, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 1],
          [0, 0, 0, 1]]

current_state = 0

def step(direction):
    global current_state
    if direction==1:
        if current_state == 7:
            current_state = 0
        else:
            current_state = current_state + 1
    else:
        if current_state == 0:
            current_state = 7
        else:
            current_state = current_state - 1
    print(states[current_state])
    GPIO.output(chan_list, states[current_state])
    time.sleep(0.005)

def dispense(steps):
    for x in range(steps):
        step(1)


def retract(steps):
    for x in range(steps):
        step(0)

def disable_stepper ():
    GPIO.output(chan_list, [0, 0, 0, 0])
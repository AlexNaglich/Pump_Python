import serial
import time
import numpy as np
from serial.tools import list_ports

# Define the stepper motor parameters
step1 = 2
dir1 = 5
multiplier1 = 1
step2 = 3
dir2 = 6
multiplier2 = 1
step3 = 4
dir3 = 7
multiplier3 = 1
totalFrequency = 50
timePerStep = 1  # seconds
timeMultiplier = 1
# direction = 1 for forward, 0 for backward
direction = 1

# Motor 1 sweeps 0 to 300 in steps of 25
# Motors 2 and 3 stay static at 100
motor2_freq = 50
motor3_freq = 50
motor1_freqs = list(range(0, 525, 25)) + list(
    range(500, -25, -25)
)  # [0, 25, 50, ..., 300]

def send_command(command):
    if ser is not None and ser.is_open:
        ser.write(command.encode())
        print(f"Sent command:\n{command}")
    else:
        print("Serial connection is not open. Cannot send command.")


# Detect which port the arduino is connected to
def find_arduino_port():
    ports = list_ports.comports()
    for port in ports:
        if "Arduino" in port.description:
            return port.device
    raise Exception("Arduino not found. Please check the connection.")


def formatStepCommand(motor1_freq):
    command1 = f"S{step1},{dir1},{int(motor1_freq*multiplier1)},{timePerStep*1000*timeMultiplier},{direction}\n"    
    command2 = f"S{step2},{dir2},{int(motor2_freq*multiplier2)},{timePerStep*1000*timeMultiplier},{direction}\n"
    command3 = f"S{step3},{dir3},{int(motor3_freq*multiplier3)},{timePerStep*1000*timeMultiplier},{direction}\n"

    return command1 + command2 + command3


# Try finally block to ensure the serial connection is closed properly even if an error occurs.
ser = None
try:
    # Connect to the arduino
    ser = serial.Serial(find_arduino_port(), 460800)
    time.sleep(2)
    # If successful, print a message
    print(f"Connected to Arduino on port: {ser.port}")

    if ser.is_open:
        time.sleep(2)

        for freq in motor1_freqs:
            command = formatStepCommand(freq)
            send_command(command)
            time.sleep(timePerStep)

finally:
    if ser is not None and ser.is_open:
        send_command("Y2,1\n")  # Stop the motors
        ser.close()

import serial
import time
import numpy as np
from serial.tools import list_ports

# Define the stepper motor parameters
step1 = 3
dir1 = 6
multiplier1 = 1.4
step2 = 2
dir2 = 5
multiplier2 = 1
# totalFrequency = np.ones(100) * 100  # Different frequencies to test
totalFrequency = [2]
timePerStep = 100  # seconds
timeMultiplier = 0
direction = 1

# Flow ratio for each step, in percentage
# flow_ratio_intro= [50, 50]
# flow_ratio_body = [75, 99, 75, 50, 25, 1, 25, 50]
# flow_ratios= flow_ratio_intro + flow_ratio_body + flow_ratio_body


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


def formatStepCommand(frequency):
    ratio = 0.5
    command1 = f"S{step1},{dir1},{int(frequency * ratio*multiplier1)},{timePerStep*1000*timeMultiplier},{direction}\n"
    command2 = f"S{step2},{dir2},{int(frequency * (1-ratio)*multiplier2)},{timePerStep*1000*timeMultiplier},{direction}\n"
    return command1 + command2


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
        for frequency in totalFrequency:
            command = formatStepCommand(frequency)
            send_command(command)
            time.sleep(
                timePerStep
            )  # Wait for 5 seconds before sending the next command


finally:
    if ser is not None and ser.is_open:
        send_command("Y2,1\n")  # Stop the motors
        ser.close()

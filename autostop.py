import serial
import time
import numpy as np
from serial.tools import list_ports

# Define the stepper motor parameters
step1 = 2
dir1 = 5
stopped = False


def send_command(command):
    if ser is not None and ser.is_open:
        ser.write(command.encode())
        # print(f"Sent command:\n{command}")
    else:
        print("Serial connection is not open. Cannot send command.")


# Detect which port the arduino is connected to
def find_arduino_port():
    ports = list_ports.comports()
    for port in ports:
        # detect usb serial devices for a microcontroller more robustly than just checking description. The description is not adequate
        if (
            "Arduino" in port.description
            or "Pico" in port.description
            or "USB Serial Device" in port.description
        ):
            return port.device

    raise Exception("Arduino or Pico not found. Please check the connection.")


# Try finally block to ensure the serial connection is closed properly even if an error occurs.
ser = None
try:
    # Connect to the arduino
    ser = serial.Serial(find_arduino_port(), 460800)
    time.sleep(2)
    # If successful, print a message
    print(f"Connected on port: {ser.port}")

    if ser.is_open:
        highest = 0
        print("Starting motors...")
        send_command("S2,5,200,0,0\n")
        while not stopped:
            send_command("RAGP26\n")  # Stop the motors
            response = ser.readline()  # Read the response from the Arduino
            cleaned_response = int(
                response.decode().strip().split(":")[-1]
            )  # Decode and clean the response
            if cleaned_response > highest:
                highest = cleaned_response
            print(f"Highest value received: {highest}")
            if highest > 500:
                stopped = True
                send_command("Y2,1\n")  # Stop the motors
                print("Stopping motors due to threshold exceeded.")


finally:
    if ser is not None and ser.is_open:
        send_command("Y10,1\n")  # Stop the motors
        ser.close()

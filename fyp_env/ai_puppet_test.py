import socket
import time
import math

UDP_IP = "127.0.0.1" 
UDP_PORT = 5052

print("🤖 Python Math Generator Online! Sending pose data at 30 FPS...")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# A variable to keep track of time for our math wave
timer = 0.0

try:
    while True:
        # Use a Sine wave to generate a number that smoothly goes up and down between 0 and 90
        # This simulates an AI generating a smooth arm movement!
        arm_angle = 45 + (math.sin(timer) * 45) 
        
        # Convert the number to a string and format it to 2 decimal places
        data_string = f"{arm_angle:.2f}"
        
        # Blast it over the network to Unity
        sock.sendto(data_string.encode(), (UDP_IP, UDP_PORT))
        
        # Increase our timer
        timer += 0.1
        
        # Pause for roughly 1/30th of a second (30 Frames Per Second)
        time.sleep(0.033)

except KeyboardInterrupt:
    print("\nTransmission stopped by user.")
import socket
import cv2
import numpy as np
import time

# Configuration
VIDEO_PATH = 'https://github.com/intel-iot-devkit/sample-videos/raw/master/car-detection.mp4'    # Use your video file
CHUNK_SIZE = 1024
DEST_IP = '127.0.0.1'
DEST_PORT = 9999

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open the video file
cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = 1 / fps if fps > 0 else 0.04

print("Streaming video...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for faster transmission
    frame = cv2.resize(frame, (320, 240))
    
    # Encode frame as JPEG
    encoded, buffer = cv2.imencode('.jpg', frame)
    data = buffer.tobytes()

    # Split into chunks and send
    for i in range(0, len(data), CHUNK_SIZE):
        chunk = data[i:i+CHUNK_SIZE]
        # Marker: 1 if last chunk else 0
        marker = 1 if i + CHUNK_SIZE >= len(data) else 0
        chunk = bytes([marker]) + chunk
        sock.sendto(chunk, (DEST_IP, DEST_PORT))

    # Sleep to maintain FPS
    time.sleep(frame_interval)

cap.release()
sock.close()
print("Streaming ended.")

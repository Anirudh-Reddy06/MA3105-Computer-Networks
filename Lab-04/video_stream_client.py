import socket
import cv2
import numpy as np

# Configuration
LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 9999
BUFFER_SIZE = 65535

# Create UDP socket and bind
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print("Client listening for video stream...")

frame_data = bytearray()

while True:
    packet, addr = sock.recvfrom(BUFFER_SIZE)
    marker = packet[0]
    data = packet[1:]
    frame_data += data

    if marker == 1:  # Last packet of frame
        # Decode frame
        npdata = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("Video", frame)

        # Clear buffer for next frame
        frame_data = bytearray()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

sock.close()
cv2.destroyAllWindows()

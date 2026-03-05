import socket
import time
import threading
from datetime import datetime
import os

# Define and create log directory
LOG_DIR = "LIKABIRD.SA/TCP/data_log"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log file paths
SEND_LOG = os.path.join(LOG_DIR, "tcp_sent.txt")
RECEIVE_LOG = os.path.join(LOG_DIR, "tcp_received.txt")

# TCP configuration
SERVER_IP = "192.168.1.201"
PORT = 5760

# Create TCP socket and connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, PORT))
print(f"Connected to TCP server: {SERVER_IP}:{PORT}")

# Send thread
def send_data():
    while True:
        current_time = str(datetime.now())
        s.send(current_time.encode('utf-8'))
        print(f"Sent: {current_time}")

        with open(SEND_LOG, "a", encoding="utf-8") as f:
            f.write(current_time + "\n")
        time.sleep(0.2)

# Receive thread
def receive_data():
    while True:
        data = s.recv(4096)
        if data:
            decoded_data = data.decode('utf-8', errors='replace').strip()
            print(f"Received: {decoded_data}")

            with open(RECEIVE_LOG, "a", encoding="utf-8") as f:
                f.write(decoded_data + "\n")

# Run threads
if __name__ == "__main__":
    t1 = threading.Thread(target=send_data)
    t2 = threading.Thread(target=receive_data)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
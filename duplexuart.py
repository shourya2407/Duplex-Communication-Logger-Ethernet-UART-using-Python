from connection import RFD900_Service
import threading
import time
import datetime
import os

LOG_DIR = "LIKABIRD.SA/UART/data_log"
os.makedirs(LOG_DIR, exist_ok=True)

# Log files
SEND_LOG = os.path.join(LOG_DIR, "uart_send.txt")
RECEIVE_LOG = os.path.join(LOG_DIR, "uart_receive.txt")

# UART settings
port = "/dev/ttyUSB0"
baud = 115200
eth_port = 5760
eth_ip = "192.168.1.201"

# RFD900 connection
def connection(port, baud):
    RFD_service = RFD900_Service.RFD900.connect(port, baud)
    return RFD_service

# Thread to receive data
def receive_from_RFD(RFD_service):
    while True:
        data = RFD900_Service.RFD900.get_data(RFD_service)
        if data:
            print(f"Received: {data}")
            with open(RECEIVE_LOG, "a", encoding="utf-8") as f:
                f.write(data + "\n")

# Thread to send data
def send_to_RFD(RFD_service):
    while True:
        current_time = str(datetime.datetime.now())
        RFD900_Service.RFD900.put_data(RFD_service, current_time)
        print(f"Sent: {current_time}")
        with open(SEND_LOG, "a", encoding="utf-8") as f:
            f.write(current_time + "\n")
        time.sleep(0.2)

# Main thread
if __name__ == "__main__":
    RFD_service = connection(port, baud)

    t1 = threading.Thread(target=receive_from_RFD, args=(RFD_service,))
    t2 = threading.Thread(target=send_to_RFD, args=(RFD_service,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

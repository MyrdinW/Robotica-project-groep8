import socket
import json


class LaptopReceiver:
    """
    LaptopReceiver is used to get signals from a laptop for movements
    """
    def __init__(self):
        host='0.0.0.0'
        port=5675
        self.s = socket.socket()
        self.s.bind((host,port))
        self.s.listen(2)

    # listens to laptop for speed and direction to return
    def listen(self):
        conn,addr= self.s.accept()
        print("Connected by",addr)
        data=conn.recv(1024)
        x = json.loads(data)
        print(x)
        conn.send(data)
        return [x["speed"], x["direction"]]

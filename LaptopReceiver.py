import socket
import json


class LaptopReceiver:

    def __init__(self):
        host='0.0.0.0'
        port=11000
        self.s = socket.socket()
        self.s.bind((host,port))
        self.s.listen(2)

    def listen(self, frame):
        conn,addr= self.s.accept()
        print("Connected by",addr)
        data=conn.recv(1024)
        x = json.loads(data)
        print(x)
        conn.send(frame)
        return [x["speed"], x["direction"]]
        
        


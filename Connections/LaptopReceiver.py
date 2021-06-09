import socket
import json


class LaptopReceiver:

    def __init__(self):
        host='0.0.0.0'
        port=5675
        self.s = socket.socket()
        self.s.bind((host,port))
        self.s.listen(2)

    def listen(self):
        conn,addr= self.s.accept()
        print("Connected by",addr)
        data=conn.recv(1024)
        x = json.loads(data)
        print(x)
        conn.send(data)
        return [x["speed"], x["direction"]]
        
        


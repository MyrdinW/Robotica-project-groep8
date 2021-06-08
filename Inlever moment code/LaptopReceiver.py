import socket
import json


class LaptopReceiver:

    def __init__(self):
        host='0.0.0.0'
        port=11001
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host,port))
        self.s.listen(2)

    def listen(self):
        conn,addr= self.s.accept()
        
        payload=conn.recv(1024)
        
        
        payload = str(payload)
        
        comp = payload.split("b'")[1].replace("')", "").replace("'", "").split(",")
        if comp[0] == '00':
                if len(comp) > 1:
                    comp = comp[1:]
                    
                    return comp
        
        


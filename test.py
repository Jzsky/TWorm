import socket, replicate, threading, time

def server():
    r = replicate.replicate("temp/replicate.py")
    data= r.getfile()
    print("start server")
    serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = "0.0.0.0"
    port = 8081
    serversocket.bind((host,port))
    serversocket.listen(5)
    print("Deployment Server listening on port", port)
    clientsocket,addr = serversocket.accept()
    print("Got a connection from", addr)
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
    clientsocket.close()
    serversocket.close()
    
def hello():
    print("start client")
    host = socket.gethostname()
    port = 8081
    serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serversocket.connect_ex(("0.0.0.0", port))
    print("Connected to server %s on port %s" % (host, port))
    time.sleep(2)
    #serversocket.close()
    
    
t1 = threading.Thread(target=server)
t2 = threading.Thread(target=hello)

# starting threads
t1.start()
t2.start()
 
    # wait until all threads finish
t1.join()
t2.join()
# with open("container/testhello.exe", 'rb') as f1:
#     data = f1.read()
#     print(data.__sizeof__())



# with open("container/testhello.exe", 'rb') as f1:
#     data = f1.read()
#     print(data.__sizeof__())

print("hello world")
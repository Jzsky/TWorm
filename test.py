import socket, replicate
r = replicate.replicate("container/testhello.exe")
data= r.getfile()

serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8081
serversocket.bind((host,port))
serversocket.listen(5)
print("Deployment Server listening on port", port)
clientsocket,addr = serversocket.accept()
print("Got a connection from", addr)
try:
    binary_content = data.read()
    chunk_size = 1024
    for i in range(0, len(binary_content), chunk_size):
        clientsocket.sendall(binary_content[i:i+chunk_size])
except FileNotFoundError:
    clientsocket.sendall(b'File not found')
except Exception:
    print("error on deploy:")
clientsocket.close()
serversocket.close()
# with open("container/testhello.exe", 'rb') as f1:
#     data = f1.read()
#     print(data.__sizeof__())
    
import socket
import sys
import time

IP = "0.0.0.0"
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)
print(f"[*] Listening on {IP}:{PORT}")
conn, addr = s.accept()
print(f"[*] Connection from {addr}")

while True:
    command = input("$ ")
    
    command += "\n"
    if "exit" in command:
        break
    
    conn.send(command.encode())
    time.sleep(1)
    ans = conn.recv(1024).decode()
    sys.stdout.write(ans)
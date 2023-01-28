import ipaddress
from icmplib import multiping
import nmap
class sniff:

    def __init__(self, ip_range:str):
        network = ipaddress.IPv4Network(ip_range)
        self.hosts = multiping([str(ip) for ip in network.hosts()], concurrent_tasks=20, privileged=False)

    def get_alive_hosts(self):
        live = []
        for host in self.hosts:
            if host.is_alive:
                live.append(host)
        return live
    
    def get_host_port_details(self, target:object, options:str):
        host = target.address
        nm = nmap.PortScanner()
        nm.scan(hosts=target.address, arguments=options)
        try: 
            for port in nm[host]['tcp']:
                print(
                    "Port:", port, 
                    "State:", nm[host]['tcp'][port]['state'], 
                    "Service:", nm[host]['tcp'][port]['name'], 
                    "Version:", nm[host]['tcp'][port]['version'])
        except Exception as e:
            pass
                

s = sniff("192.168.56.113")
for host in s.get_alive_hosts():
   if host.address == "192.168.56.113":
       s.get_host_port_details(host,"-sV")


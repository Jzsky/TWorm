import ipaddress
from icmplib import multiping
import nmap3, psutil, socket, struct

class sniff:

    def __init__(self):
        self.network = self.get_network_info()
        self.hosts = self.hosts_detection()
        self.infected = {}

    def external_sniff(self, target_range:str):
        if "/" in target_range:
            sub_network = target_range.split("/")
            ip_range = self.get_ip_range(sub_network[0],sub_network[1])
        else:
            ip_range = [target_range]
        targets = multiping(ip_range, concurrent_tasks=20, privileged=False)
        return targets

    def get_network_info(self):
        interfaces = []
        interface_info = psutil.net_if_addrs()
        for interface, addrs in interface_info.items():
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith("127"):
                    #Testing only on 192
                    if addr.address.startswith("192"):
                        interfaces.append((interface, addr.address, addr.netmask))
        return interfaces
    
    def get_ip_range(self, ip_address, subnet_mask):
        try:
            network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
            return [str(ip) for ip in list(network.hosts())]
        except Exception as e:
            return []
    
    def hosts_detection(self):
        hosts = {}
        for interface, ip_address, netmask in self.network:
            ip_range = self.get_ip_range(ip_address,netmask)
            targets = multiping(ip_range, concurrent_tasks=20, privileged=False)
            hosts[ip_address] = targets
        return hosts

    def get_alive_hosts(self, local_inter_ip):
        live = []
        for host in self.hosts[local_inter_ip]:
            if host.is_alive:
                live.append(host)
        return live
    
    def get_host_port_details(self, target:object)->dict:
        try:
            nmap = nmap3.Nmap()
            #need to change if want to scan more ports
            version_result = nmap.nmap_version_detection(target.address,args="-p 1-1024")
            return version_result
        except Exception as e:
            print("Errors on port scanning - {}".format(e))
            return {}

    def get_host_os_details(self, target:object)->dict:
        try:
            nmap = nmap3.Nmap()
            ostype = nmap.nmap_os_detection(target.address)
            if ostype["error"]:
                return {}
            return ostype
        except Exception as e:
            print("Errors on OS Scan -> Possbile Privilege issues: g{}".format(e))
            return {}

    def get_interface_network(self):
        return self.network

    def get_host_networks(self):
        return self.hosts

    def is_vulnerable(self, cur, port_info):

        cur.execute("")
        
        pass




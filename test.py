import psutil, socket, struct
import ipaddress

def get_network_info():
    interfaces = []
    interface_info = psutil.net_if_addrs()
    for interface, addrs in interface_info.items():
        for addr in addrs:
            #only testing with 192
            if addr.family == socket.AF_INET and not addr.address.startswith("127"):
                if addr.address.startswith("192"):
                    interfaces.append((interface, addr.address, addr.netmask))
    return interfaces

def get_ip_range(ip_address, subnet_mask):
    try:
        network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
        return [str(ip) for ip in list(network.hosts())]
    except Exception as e:
        return []

network_info = get_network_info()
for interface, ip, mask in network_info:
    print("Interface:", interface)
    print("IP address:", ip)
    print("Subnet mask:", mask)
    #hosts = get_ip_range(ip,mask)
    #print(hosts)
    print("---")
    


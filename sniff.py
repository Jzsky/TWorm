import ipaddress
from icmplib import multiping
import nmap3, psutil, socket, struct

class sniff:

    # initilize the sniff object
    def __init__(self):
        # get current machine network information
        self.network = self.get_network_info()
        # scan all the hosts on current network
        self.hosts = self.hosts_detection()
        self.infected = {}

    #unimplemented features - external scanner 
    def external_sniff(self, target_range:str):
        if "/" in target_range:
            sub_network = target_range.split("/")
            ip_range = self.get_ip_range(sub_network[0],sub_network[1])
        else:
            ip_range = [target_range]
        targets = multiping(ip_range, concurrent_tasks=20, privileged=False)
        return targets

    # gather network information on current machine
    def get_network_info(self):
        interfaces = []
        interface_info = psutil.net_if_addrs()
        # loop through network interfaces and ip address
        for interface, addrs in interface_info.items():
            #loop though ip addresses in each network interfaces
            for addr in addrs:
                #skip if it is 127 loop back ip address
                if addr.family == socket.AF_INET and not addr.address.startswith("127"):
                    #in testing environment - only testing on network interface 192.168
                    if addr.address.startswith("192.168"):
                        #add the ip addresses on the list
                        interfaces.append((interface, addr.address, addr.netmask))
        return interfaces
    
    # get a list of ips base on provided ip and subnet mask 
    def get_ip_range(self, ip_address, subnet_mask):
        try:
            network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
            return [str(ip) for ip in list(network.hosts())]
        except Exception as e:
            return []
    
    # detection the status of the hosts on the network, alive or down
    def hosts_detection(self):
        hosts = {}
        for interface, ip_address, netmask in self.network:
            ip_range = self.get_ip_range(ip_address,netmask)
            targets = multiping(ip_range, concurrent_tasks=20, privileged=False)
            hosts[ip_address] = targets
        return hosts

    # return a lists of live hosts
    def get_alive_hosts(self, local_inter_ip):
        live = []
        for host in self.hosts[local_inter_ip]:
            if host.is_alive:
                live.append(host)
        return live
    
    # return port details with provided ports to scan
    def get_host_port_details(self, target:object, scan_ports)->dict:
        try:
            #use nmap technique
            nmap = nmap3.Nmap()
            #need to change if want to scan more ports
            version_result = nmap.nmap_version_detection(target.address,args="-p {}".format(",".join(scan_ports)))
            return version_result
        except Exception as e:
            print("Errors on port scanning - {}".format(e))
            print("Try alternative method")
            #use basic socket scan for banner when nmap is not available
            version_result = self.get_host_port_details_native(target, options="-p {}".format(",".join(scan_ports)))
            return version_result
    
    # parse the details on the return banner response
    def parse_service_details(self, response, service):
        product = ""
        version = ""
        extrainfo = ""
        method = ""
        conf = ""
        native = response

        service["product"] = product
        service["version"] = version
        service["extrainfo"] = extrainfo
        service["method"] = method
        service["conf"] = conf
        service["native"] = native
        return service

    #tcp socket banner grabber
    def get_host_port_details_native(self, target:object, options)->dict:
        try:
            option = options.split(" ")
            if "-p" == option[0]:
                ports = option[1].split(",")
            result = {target.address:{"osmatch":{},"ports":[]}}
            for port in ports:
                print("scanning on port: {}".format(int(port)))
                try:
                    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    sock.settimeout(3)
                    #sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 64)
                    conn = sock.connect_ex((target.address,int(port)))
                    #ttl = sock.getsockopt(socket.IPPROTO_IP,socket.IP_TTL)
                    if conn == 0:
                        #print(socket.getservbyport(port))
                        #print("Port {} is open".format(port))
                        try:
                            response = sock.recv(1024).decode()
                        except TimeoutError:
                            response = ""
                        #init service
                        service = {
                                    "name": socket.getservbyport(int(port)),
                                    "product": "",
                                    "version": "",
                                    "extrainfo": "",
                                    "method": "",
                                    "conf": "",
                                    "native": ""
                                    }

                        paresed_service = self.parse_service_details(response, service)

                        port_info = {
                            "protocol": "tcp",
                            "portid": port,
                            "state": "open",
                            "reason": "syn-ack",
                            #"reason_ttl": str(ttl),
                            "service": paresed_service,
                            "cpe": [
                                {
                                    "cpe": "",
                                }
                            ],
                            "scripts": []
                            }
                        result[target.address]['ports'].append(port_info)
                    sock.close()
                except socket.error as e:
                    print("socket error: {}".format(e))
            return result
        except Exception as e:
            print("alternative method failed: {}".format(e))
        return {}
            
    # unimplemented for target host operating system scan
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

    # return network interface information
    def get_interface_network(self):
        return self.network

    # return hosts informations on the network
    def get_host_networks(self):
        return self.hosts

    def is_vulnerable(self, port_info):
        pass

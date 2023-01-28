import socket
import ipaddress
from icmplib import multiping
class sniff:

    def __init__(self, ip_range:str):
        network = ipaddress.IPv4Network(ip_range)
        #self.hosts = multiping([str(ip) for ip in network.hosts()], privileged=False)

    def get_alive_hosts(self):
        live = []
        for host in self.hosts:
            if host.is_alive:
                live.append(host)
                print(host)
        return live
    
    def get_host_details(self, target:object, start_port:int, end_port:int):
        print("report for {}:".format(target))
        for port in range (start_port, end_port+1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((target,port))
                
                if result == 0:
                    
                    try:
                        sock.send(b'GET / HTTP/1.1\r\n')
                        response = sock.recv(1024).decode()
                        service = get_service_name(response)
                        print("Port {} open -> Serive: {}".format(port,service))
                    except Exception as e:
                        print("fail")
                sock.close()
            except Exception as e:
                pass
        
        def get_service_name(response:str):
            return response

s = sniff("192.168.86.0/24")
#print(s.get_alive_hosts())
s.get_host_details('192.168.1.244',1,1023)




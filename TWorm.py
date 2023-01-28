from socket import *
from os import system as sys
import time
startTime = time.time()

def main():
    targets = '192.168.56.102'
    t_IP=gethostbyname(targets)
    for port in range(1,1024):
        scan=socket(AF_INET, SOCK_STREAM)
        scan.settimeout(0.001)
        connection=scan.connect_ex((t_IP,port))
        if ( connection == 0 ):
            # scan.settimeout(None)
            # scan.send(b'test')
            # data = scan.recv(1024)   
            data=""
            print ( "Port {}: Open -> Service: {}".format(port, repr(data)) )
        scan.close()
    print('Time taken:', time.time() - startTime)


if __name__=='__main__':
    main()
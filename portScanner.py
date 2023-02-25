#!/usr/bin/python3

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def check_ports(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket object to connect to
    client.settimeout(2) # default timeout to close connections if they are successful
    try:
        client.connect((host, port)) # attempts to connect to given port
        return True # returns true if connection is successful
    except:
        return False # returns false if connection is unsuccessful
        
# scan port numbers on a host
def scan_ports(host, ports, threads):
    print(f'Scanning IP: {host} , Ports: {ports[0]} to {ports[-1]} with {threads} threads...')
    with ThreadPoolExecutor(threads) as executor: # assigning ThreadPoolExecutor with argument length of list of ports as max_workers to variable name 'executor'
        results = executor.map(check_ports, [host]*len(ports), ports) 
        # Calling the executor.map function with arguments check_ports function, a list of hosts multiplied by the length of the ports list, and the ports list. 
        # This concurrently runs the check_ports function against the lists of hosts and ports using threads allocated by ThreadPoolExecutor.
        # Default value of max_workers is changed to min(32, os.cpu_count() + 4). 
        # This default value preserves at least 5 workers for I/O bound tasks. 
        # It utilizes at most 32 CPU cores for CPU bound tasks which release the GIL. 
        # And it avoids using very large resources implicitly on many-core machines.)
        for port,is_open in zip(ports,results): # assigns previous true or false value to a list of values containing sublists with the port number and the True or False value if a port is Open or Closed
            if is_open:
                print(f'PORT: {port} is open') # if previous is_open is true, print port is open

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A multi-threaded port scanner written in python', formatter_class=argparse.RawDescriptionHelpFormatter, epilog='Example: portScanner.py 127.0.0.1 -p 1-1024')
    parser.add_argument('target', help='The target IP address to be scanned')
    parser.add_argument('-p', '--ports', help='The range of ports to be scanned, separated by \'-\', or a list of ports separated by \',\'')
    parser.add_argument('-t', '--threads', type=int, help='The max number of threads to use. Default is max available to ThreadPoolExecutor')
    args = parser.parse_args() # command line arguments assigned and defined above
    target = args.target
    
    if args.ports != None and '-' in args.ports: # if there is a dash in the ports value, change the port values to a list including all ports between minimum and maximum port values plus one
        [min_p, max_p] = [int(i) for i in args.ports.split('-')]
        ports = range(min_p, max_p + 1)
    elif args.ports != None: # if the ports argument does not contain a dash, change port values to a list of defined port values separated by a comma
        ports = [int(i) for i in args.ports.split(',')]
        
    if args.threads == None:
        threads = len(ports)
    elif args.threads > len(ports):
        print('Too many threads for this scan!')
        sys.exit()
    else:
        threads = args.threads
    
    try:
        scan_ports(target, ports, threads)
    except KeyboardInterrupt: # handle ctrl-c
        print('Scan cancelled by user!')
        sys.exit()
    

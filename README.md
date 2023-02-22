# threadedportscanner
My multi-threaded port scanner written in python

This port scanner uses command line arguments to check if a range of ports at a given IP are open or closed.

Running python3 portScanner.py -h will display

      Usage: portScanner.py [-h] [-p PORTS] target

      A multi-threaded port scanner written in python

      positional arguments:
      target The target IP address to be scanned

      options:
      -h, --help show this help message and exit

      -p PORTS, --ports PORTS The range of ports to be scanned, separated by '-', or a list of ports separated by ','

      Example: portScanner.py 127.0.0.1 -p 1-1024

The multi-threading is handled by the python class concurrent.futures.ThreadPoolExecutor
This module allocates threads automatically and, using the .map function, will run the port_scan function against a number of ports concurrently.

This program does not currently integrate with nmap, and does not provide details on why a port is open or closed. 
It is a very basic functionality, where the program attempts to make a connection to a defined port, and if that connection is successful, returns True.
If it is unsuccessful, it returns False and ignores that port. Because of this, it will not work well against filtered ports or firewalls.

This program isn't meant as a replacement for rustscan, which I definitely recommend as the number one multi-threaded port scanner.
It is purely written to demonstrate the authors ability to write a program capable of quickly scanning a network.

Credit to https://superfastpython.com/threadpoolexecutor-port-scanner/ for guidance on the use of ThreadPoolExecutor.
This guide helped me write my program, however my code allows command line arguments to be passed to the program making it more user friendly.

DISCLAIMER: The author does not approve of the programs use in any way shape or form that breaks any laws or terms of service.

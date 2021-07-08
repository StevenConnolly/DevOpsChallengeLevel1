#!/usr/bin/python3

# Import modules from python standard library. Doesn't require additional downloads
import time # allows for sleep
from datetime import datetime # allows for timestamp

######################################################################################################################################
#   While loop that will loop indefinitely every 10 seconds.
#   "/proc/net/tcp" will be opened and the local and remote ipv4 addresses (including ports) will be converted to required output 
#   Combine the ipv4 address into 1 string "192.0.2.56:5973 -> 10.0.0.5:80" and add to uniqueConnections set.
#   Only print new connections after the each 10 second delay.
#   Sample output: 2021-04-28 15:28:05: New connection: 192.0.2.56:5973 -> 10.0.0.5:80
#######################################################################################################################################

''' Python int() function you can declare a base as the second value. Hex is base 16 but the numbers still need to be reversed since they are in 
little endian. This will only apply to the ip address. TCP/IP is in big endian format so the ports only need a simple hex conversion using the int() function'''

# The function below converts the IP address to IPv4 decimal format

def littleEndianIp(hexip):

  ''' - join(): takes iterable items and joins them into a string with a separator
      - str(): converts the value into a string
      - int(): takes 2 objects and returns an integer (value, base)
      - reversed(): returns the reversed iterator of a sequence
      - range(): iterates over a range: 1st value is starting point, 2nd value is ending point, 3rd value (optional) is the step. A step of 2 here iterates every 2 numbers in the hex IP
      - len(): counts the length of a string
      
      In a loop, the little endian hex is split into pairs of 2 based on the index, converted to hex, reversed in order then joined together with a "." separator.
      ex. 0100007F -> 01 00 00 7F -> 1 0 0 127 -> 127 0 0 1 -> 127.0.0.1'''

  return ".".join(str(int(i, 16)) for i in reversed([hexip[i:i+2] for i in range(0, len(hexip), 2)]))
  

''' An empty set named uniqueConnections that will store new connections between the local ipv4 address and the remote ipv4 address.
Sets store unordered unique values only. Objects in the set are immutable. This will ensure only new connections are placed in the set and the duplicates are ignored. Now when the file is reopened only the new connections are accepted.
'''

uniqueConnections = set()

'''While loop that runs on a condition. The condition is True so it will run until the program is exited'''

# Create a loop that will run indefinetely. This is done with the While True: statement
while True:
  try:
    # try and open the file. r is for read only
    with open("/proc/net/tcp","r")as tcpLog:

    # Read each line of the file in a loop
      for line in tcpLog.readlines():

        ''' The ip address and port needs to be converted in different formats. The line is split into strings. Strings containing 
        an ":" are split in 2 in order to translate the IP and port. 
        ex. "0: 00000000:1F99 00000000:0000" becomes "0" "00000000" "1F99" "00000000" "0000" '''

        tcpLine = [ x.strip() for x in line.replace(":"," ").split() ]

        # First line in file needs to be skipped. If line begins with a-z, continue
        if tcpLine[0].isalpha():
          continue

        # Translate the IP and port using the littleEndianIp function. 
        # Assign variables for the connections and ports
        
        localConn = littleEndianIp(tcpLine[1])
        localPort = str(int(tcpLine[2],16))
        remoteConn = littleEndianIp(tcpLine[3]) 
        remotePort = str(int(tcpLine[4],16))
        
        # add connections and ports into 1 string called localRemoteConnection
        # output: " New connection: 192.0.2.56:5973 -> 10.0.0.5:80"
        localRemoteConnection =  " New connection: " + localConn + ":" + localPort + " -> " + remoteConn + ":" + remotePort
        
        # Add timestamp with appropriate formatting
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # print output with timestamp
        print(now + ":" + localRemoteConnection)
    
      # Sleep for 10 seconds
      time.sleep(10)

  # Error check. If file "/proc/net/tcp" not found exit with message
  except IOError:  
    print("File doesn't exist. This program is intended for Linux systems only. Check system and ensure its running properly")
    exit()

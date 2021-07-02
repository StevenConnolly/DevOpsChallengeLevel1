# DevOps Development Challenge

## Level 1 Challenge
Write a program that reads `/proc/net/tcp` every 10 seconds, and reports any new connections. 

Sample Output:
```
2021-04-28 15:28:05: New connection: 192.0.2.56:5973 -> 10.0.0.5:80
2021-04-28 15:28:05: New connection: 203.0.113.105:31313 -> 10.0.0.5:80
2021-04-28 15:28:15: New connection: 203.0.113.94:9208 -> 10.0.0.5:80
2021-04-28 15:28:15: New connection: 198.51.100.245:14201 -> 10.0.0.5:80
```

# ipConnections Python Script
## Overview
The project will be a python script called `ipConnections.py` that opens and reads `/proc/net/tcp` in a 10 second loop. 

## The problem at hand
The `/proc/net/tcp` lists all listening TCP sockets, and next lists all established
TCP connections. The problem is that the output of the ipv4 local and remote connections are in little endian which is the default on x86 architectures. TCP/IP uses big endian so the local_address and rem_address strings needs to be split.
```
❯ cat /proc/net/tcp
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 00000000:1F99 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 30876 1 0000000000000000 100 0 0 10 0
   1: 00000000:DFF9 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 22564 1 0000000000000000 100 0 0 10 0
   2: 00000000:BDDB 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 22572 1 0000000000000000 100 0 0 10 0
   3: 00000000:0801 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 15863 1 0000000000000000 100 0 0 10 0
   4: 0100007F:8287 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 26899 1 0000000000000000 100 0 0 10 0
   5: 00000000:98CB 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 15877 1 0000000000000000 100 0 0 10 0
  ```
ex. 
0100007F:0050 needs to translate to 127.0.0.1:80
E10FA20A:01BB needs translate to 10.162.15.225:443

## How will it be done?
The script will read the file line by line and parse it by separating each line into individual strings. 
The `:` will be removed and the string split in two. This allows the translating of big and little endians individually.<br />
ex line:  <br />
```0: 00000000:1F99 00000000:0000 0A 00000000:00000000 00:00000000 00000000 0 0 30876 1 0000000000000000 100 0 0 10 0```<br />
into: <br />
``` `0` `00000000` `1F99` `00000000` `0000` `0A` `00000000` `00000000` `00` `00000000` `00000000` `0` `0` `30876` `1` `0000000000000000` `100` `0` `0` `10` `0` ```

The indexes for the strings of local IP, local port, remote IP, remote port will be used to perform the translation. Local IP, local port, remote ip, remote port are found at `index 1,2,3,4` respectively.

The int() function in python allows for the input of a base which makes translating the port easy. Running int(i, 16) will give the hex (base 16) of the first input. ex. `int(0050, 16) = 80.`

The little endian is trickier since it needs to be converted from `0100007F` to `1.0.0.127` and then reversed to `127.0.0.1`. This is done by creating a small function that splits the hex little endian (ex 0100007F) into byte pairs and converts them. <br />
    ex converting 0100007F:  <br />
       `01 -> 1` <br />
       `00 -> 0` <br />
       `00 -> 0`  <br />
       `7F -> 127`<br />

Then using the reverse() function in python as you'd guess, you can reverse the order of the string. This will be done in combination with the join() function. This will combine the reversed strings together and add decimals in between. From `1 0 0 127` to `127.0.0.1`

Once the local and remote connections have been translated to decimal format they are joined together as 1 string <br />
ex. 
`"192.0.2.56:5973 -> 10.0.0.5:80"` named `localRemoteConnection`

An empty set() will be created and the `localRemoteConnection` string will be added to the set. Python sets only allow for unique values so this will stop duplicate connections from being added.

The script will check to see if new `localRemoteConnection` on each line is in the set and add it if it isn't. <br />
The output required is `2021-04-28 15:28:15: New connection: 198.51.100.245:14201 -> 10.0.0.5:80`.<br />

This is accomplished by adding a timestamp with "New Connection:" text and the `localRemoteConnection` string.
The program will run in a 10 second loop indefinitely outputting only new connections found. 


# How to Install Project
## Files needed:
Download the repo from GitHub 
`git clone https://github.com/StevenConnolly/DevOpsChallengeLevel1.git`
## Requirements
Python3 is the only thing that needs to be installed on the system
### Ubuntu/Debian
`❯  apt install -y python3`
###  CentOS/RHEL
`❯  yum install -y python3`


# How to Use Your Project
You can run the script with your choice of the following commands:
## First:
`❯  cd DevOpsChallengeLevel1`
## Then:
`❯  python3 ipConnections.py`
### OR
`❯ chmod +x ipConnections.py`<br />

to make it executable:<br />
`❯  ./ipConnections.py`


# Questions
## 1. How would you prove the code is correct?
To prove the code is correct you can verify the ip connections discovered by using the netstat or ss commands. 
They too discover active connections. Running `netstat -vatn` will show all current tcp connections similar to the code submitted. 
## 2. How would you make this solution better? 
Removing the 10 second sleep command will avoid a delay in finding new connections. The program is running with a `While True` loop which will continue to open the file without delay indefinitely. Having a sleep command of 10 seconds limits how often the script can open the file.
## 3. Is it possible for this program to miss a connection?
The program is running in a 10 second loop and /proc/net/tcp is only showing active connections so it's possible a connection came and went during those 10 seconds and the program missed the connection.
## 4. If you weren't following these requirements, how would you solve the problem of logging every new connection? 
If I didn't have to follow the requirements I would enable logging in iptables instead. `iptables -A INPUT -j LOG`. This will output the connections to `/var/log/kern.log` (on Ubuntu/Debian) or `/var/log/messages` (on CentOS/RHEL). The output is already in ipv4 decimal format so it doesn't require any translation. Another alternative would be to `tail -f /proc/net/tcp` and translate the output. 




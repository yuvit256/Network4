# Networks_Assignment_4
## In this assignment we wrote three program files: 
+ ping.py 
+ better_ping.py
+ watchdog.py

# ping.py:
The program will send an ICMP ECHO REQUEST to the host, and when receiving ICMP-ECHO-REPLY, the program will send the next ICMP ECHO REQUEST.
For each packet received, we will print the packet IP, packet sequence number, and time between the request and replay.

# better_ping.py:
We modify the ping program, and write a watchdog that will hold a timer (TCP connection on port 3000) to ensure that if we don’t receive an ICMP-ECHO-REPLY after sending an ICMP-REQUEST for 10 seconds, it will exit and print "server <ip> cannot be reached."

# watchdog.py:
Watchdog is a timer to detect and recover your computer dis-functions or hardware fails. It’s a chip whose sole purpose is to receive a signal every millisecond from the CPU. It will reboot the system if it hasn’t received any signal for 10 milliseconds (mostly when hardware fails).

## Authers: Ron Yacobovich & Yuval Musseri

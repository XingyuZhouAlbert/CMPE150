Shawn Chumbar
Professor Christina Parsa
CMPE 150
Lab 3 Readme

Included Files:
lab3.pdf
lab3controller.py
README.txt

This assignment is trying to mimic a firewall with the following rules:
######################################################################################################
#						Rules:
# 1. Allow any ARP traffic.
# 2. Allow any ICMP traffic.
# 3. TCP traffic should be allowed between h1 and h3 (both h1 to h3 and h3 to h1).
# 4. Any other traffic should be dropped irrespective of the protocol.
######################################################################################################
Useful Resources:
# http://intronetworks.cs.luc.edu/auxiliary_files/mininet/poxwiki.pdf
# https://en.wikipedia.org/wiki/EtherType
# http://csie.nqu.edu.tw/smallko/sdn/iperf_mininet.htm
# http://sdnhub.org/tutorials/pox/
# https://github.com/matt-welch/POX_Firewall/blob/master/Firewall.py
 --The github above helped me understand what was going on. Just seeing another person use the methods helped
   me understand how to do some of the function calls
# https://openflow.stanford.edu/display/ONL/POX+Wiki
# https://openflow.stanford.edu/display/ONL/POX+Wiki.html#POXWiki-MatchStructure
# Modified Supplemental Instruction (MSI)


Extra Comments/Concerns:
This lab was very difficult. I was not able to start on it early due to the fact that I had a midterm on 
Friday. 
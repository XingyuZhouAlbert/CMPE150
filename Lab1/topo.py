#!/usr/bin/python

# Shawn Chumbar (schumbar)
# Schumbar@ucsc.edu
# ID# 1470937

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

class MyTopology(Topo):
    """
    A basic topology
    """
    def __init__(self):
        Topo.__init__(self)

        # Set Up Topology Here
        #========Switches========
        switch1 = self.addSwitch('s1')    ## Adds a Switch
        switch2 = self.addSwitch('s2')

        #========Hosts========
        host1 = self.addHost('h1')       ## Adds a Host
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        host4 = self.addHost('h4')

        #========Links======== ## Add a link
        self.addLink(host1, switch1)   # (h1, s1)
        self.addLink(host2, switch1)   # (h2, s1)  h1->s1, h2->s1
        self.addLink(host3, switch2)   # (h3, s2)  
        self.addLink(host4, switch2)   # (h4, s2)  h3->s2, h4->s2
        self.addLink(switch1, switch2) # (s1, s2)  h1->s1, h2->s1, s1->s2, h3->s2, h4->s2

if __name__ == '__main__':
    """
    If this script is run as an executable (by chmod +x), this is
    what it will do
    """

    topo = MyTopology()            ## Creates the topology
    net = Mininet( topo=topo )        ## Loads the topology
    net.start()                      ## Starts Mininet

    # Commands here will run on the simulated topology
    CLI(net)

    net.stop()                       ## Stops Mininet
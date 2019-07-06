#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    h1 = self.addHost('h10',mac='00:00:00:00:00:01',ip='10.0.1.10/24', defaultRoute="h10-eth0") # Host 10
    h2 = self.addHost('h20',mac='00:00:00:00:00:02',ip='10.0.2.20/24', defaultRoute="h20-eth0") # Host 20
    h3 = self.addHost('h30',mac='00:00:00:00:00:03',ip='10.0.3.30/24', defaultRoute="h30-eth0") # Host 30
    h4 = self.addHost('serv',mac='00:00:00:00:00:04',ip='10.0.4.10/24', defaultRoute="serv-eth0") # Server
    h5 = self.addHost('trusted',mac='00:00:00:00:00:05',ip='104.82.214.112/24', defaultRoute="trusted-eth0") # Trusted Host
    h6 = self.addHost('untrusted',mac='00:00:00:00:00:06',ip='156.134.2.12/24', defaultRoute="untrusted-eth0") # Untrusted Host

    # Create a switch. No changes here from Lab 1.
    s1 = self.addSwitch('s1') # Floor 1 Switch
    s2 = self.addSwitch('s2') # Floor 2 Switch
    s3 = self.addSwitch('s3') # Floor 3 Switch
    s4 = self.addSwitch('s4') # Data Center Switch
    s5 = self.addSwitch('s5') # Core Switch

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    
    
    # H10->FS1->CS
    self.addLink(h1,s1, port1=0, port2=1) # Host 10 to Floor 1 Switch
    self.addLink(s5,s1, port1=1, port2=2) # Floor 1 Switch to Core Switch
    print("Connection 1")
    
    #H20->FS2->CS
    self.addLink(h2,s2, port1=0, port2=1) # Host 20 to Floor 2 Switch
    self.addLink(s2,s5, port1=2, port2=2) # Floor 2 Switch to Core Switch
    # print("C2")
    #H30->FS3->CS
    self.addLink(h3,s3, port1=0, port2=1) # Host 30 to Floor 3 Switch
    self.addLink(s3,s5, port1=2, port2=3) # Floor 3 Switch to Core Switch
    # print("C3")
    #Server->DCS->CS
    self.addLink(h4,s4, port1=0, port2=1) # Server to Data Center Switch
    self.addLink(s4,s5, port1=2, port2=6) # Data Center Switch to Core Switch
    # print("c4")
    #TH->CS
    self.addLink(h5,s5, port1=0, port2=4) # Trusted Host to Core Switch
    # print("C5")
    # UTH->CS
    self.addLink(h6,s5, port1=0, port2=5) # Untrusted Switch to Core Switch
    #print("C6")

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()


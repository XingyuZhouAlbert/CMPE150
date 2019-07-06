"""
Shawn Chumbar
CMPE 150: Professor Christina Parsa
Final Lab: finalcontroller_skel.py
"""

# Final Skeleton
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
	"""
	A Firewall object is created for each switch that connects.
	A Connection object for that switch is passed to the __init__ function.
	"""
	def __init__ (self, connection):
		# Keep track of the connection to the switch so that we can
		# send it messages!
		self.connection = connection

		# This binds our PacketIn event listener
		connection.addListeners(self)

	def do_final (self, packet, packet_in, port_on_switch, switch_id):
		# This is where you'll put your code. The following modifications have 
		# been made from Lab 4:
		#   - port_on_switch represents the port that the packet was received on.
		#   - switch_id represents the id of the switch that received the packet
		#      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
		# Making and Installing table entry
		msg = of.ofp_flow_mod()
                # match packet
		msg.match = of.ofp_match.from_packet(packet)
                msg.idle_timeout = 30
		msg.hard_timeout = 30  

		# Declare the different IP Addresses so it is easier to code
		host10_IP        = '10.0.1.10' # Host10 IP address
		host20_IP        = '10.0.2.20' # Host20 IP address 
		host30_IP        = '10.0.3.30' # Host30 IP address
		server_IP        = '10.0.4.10' # Server IP address
		trustedHost_IP   = '104.82.214.112' # Trusted Host IP address
		untrustedHost_IP = '156.134.2.12' # Untrustest Host IP address

		# set up variables that will make it easier to name the different switches
		floorSwitch1 = 1 # Floor 1 Switch
		floorSwitch2 = 2 # Floor 2 Switch
		floorSwitch3 = 3 # Floor 3 Switch
		dataCenterSwitch = 4 # Data Center Switch
		coreSwitch = 5 # Core Switch
		# Find the various different parts of the packet
		isARP = packet.find('arp')
		isTCP = packet.find('tcp')
		isICMP = packet.find('icmp')
		check_IPV4 = packet.find('ipv4')
		
                if isARP is not None: #check if ARP is not None
			print("\nARP")
			msg.data = packet_in #set the packet data
			msg.match.dl_type = 0x0806 #Set the data link type
			action = of.ofp_action_output(port=of.OFPP_FLOOD) #FLOOD
			msg.actions.append(action) #append action, then send
			self.connection.send(msg)
		else: #We know that the packet is using some sort of IP protocol
			if isICMP is not None: #if we are using ICMP
				print("\nICMP:")
				##########################
				#########SWITCH 1#########
				##########################
				if switch_id == floorSwitch1: # We are in floor Switch 1
					msg.data = packet_in #Set the data
					if check_IPV4.dstip == host10_IP:#Try to send to Host10
						msg.actions.append(of.ofp_action_output(port = 1)) #Output to port 1
						self.connection.send(msg) #send the message
					else: #trying to send to Core Switch
						msg.actions.append(of.ofp_action_output(port = 2)) #if its not host10, send it everywhere else
						self.connection.send(msg)
		
				##########################
				#########SWITCH 2#########
				##########################
				elif switch_id == floorSwitch2: # We are now inside of floor Switch 2
					msg.data = packet_in
					if check_IPV4.dstip == host20_IP:#Try to send to Host20
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
					else: #Trying to send to Core Switch (if sending to host other than Host20)
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)
		
				##########################
				#########SWITCH 3#########
				##########################
				elif switch_id == floorSwitch3: #We are now in Floor Switch 3
					msg.data = packet_in
					if check_IPV4.dstip == host30_IP:#Try to send to Host30
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
					else: #Trying to send packets to Core Switch
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)
		
				##########################
				####DATA CENTER SWITCH####
				##########################
				elif switch_id == dataCenterSwitch: #We are now in Data Center Switch
					msg.data = packet_in
					if check_IPV4.dstip == server_IP: #Trying to send data to server
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
					else: #Trying to send data to Core Switch
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)

				##########################
				#######CORE  SWITCH#######
				##########################
				elif switch_id == coreSwitch: #We are now in Core Switch
					msg.data = packet_in
                                        if check_IPV4.dstip == untrustedHost_IP: #If the destination is untrustedHost
                                                msg.actions.append(of.ofp_action_output(port = 5))
                                                self.connection.send(msg)
                                        elif check_IPV4.srcip == untrustedHost_IP and check_IPV4.dstip == trustedHost_IP: #untrustedHost->trustedHost
                                                msg.actions.append(of.ofp_action_output(port = 4))
                                                self.connection.send(msg)
                                        elif check_IPV4.srcip == untrustedHost_IP: #untrustedHost->Any Host (Block this)
                                        	print("\nBLOCK") 
                                                #msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))
                                                self.connection.send(msg)
                                        elif check_IPV4.dstip == host10_IP: #Trying to send data to Host10 (AnyHost->Host10)
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
					elif check_IPV4.dstip == host20_IP: #Trying to send data to Host20 (AnyHost->Host20)
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)
					elif check_IPV4.dstip == host30_IP: #Trying to send data to Host30 (AnyHost->Host30)
						msg.actions.append(of.ofp_action_output(port = 3))
						self.connection.send(msg)
					elif check_IPV4.dstip == trustedHost_IP: #Trying to send data to Trusted Host (AnyHost->trustedHost)
						msg.actions.append(of.ofp_action_output(port = 4))
						self.connection.send(msg)
					elif check_IPV4.dstip == untrustedHost_IP: #Trying to send data to Untrusted Host (AnyHost->untrustedHost)
						msg.actions.append(of.ofp_action_output(port = 5))
						self.connection.send(msg)
					elif check_IPV4.dstip == server_IP: #Trying to send data to Server (AnyHost->Server)
						msg.actions.append(of.ofp_action_output(port = 6))
						self.connection.send(msg)
					else: #BLOCK any packet that does not follow these rules
						print("\nBLOCK")
						#msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))
						self.connection.send(msg)

                        ########## TCP ###########      
                        elif isTCP is not None:
                                print("\nTCP")
                                msg.nw_proto = 6 #6 for TCP
                        	if switch_id == floorSwitch1: # We are in floor Switch 1
                        		msg.data = packet_in
					if check_IPV4.dstip == host10_IP:#Try to send to Host10
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
					else: #trying to send to Core Switch
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)
		
				##########################
				#########SWITCH 2#########
				##########################
				elif switch_id == floorSwitch2: # We are now inside of floor Switch 2
					msg.data = packet_in
					if check_IPV4.dstip == host20_IP:#Try to send to Host20
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
						#sendPort(self, packet, packet_in, port_on_switch, switch_id, 1)
					else: #Trying to send to Core Switch
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)
		
				##########################
				#########SWITCH 3#########
				##########################
				elif switch_id == floorSwitch3: #We are now in Floor Switch 3
					msg.data = packet_in
					if check_IPV4.dstip == host30_IP:#Try to send to Host30
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
					else: #Trying to send packets to Core Switch
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)
		
				##########################
				####DATA CENTER SWITCH####
				##########################
				elif switch_id == dataCenterSwitch: #We are now in Data Center Switch
					msg.data = packet_in
					if check_IPV4.dstip == server_IP: #Trying to send data to server
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
					else: #Trying to send data to Core Switch
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)

				##########################
				#######CORE  SWITCH#######
				##########################
				elif switch_id == coreSwitch: #We are now in Core Switch
					msg.data = packet_in
                                        if check_IPV4.srcip == untrustedHost_IP and check_IPV4.dstip == server_IP: #untrusted->server
                                                #Drop the packet
                                                self.connection.send(msg)
                                        elif check_IPV4.srcip == server_IP and check_IPV4 == untrustedHost_IP: #Server->untrustedHost
                                                #send the packet
                                                msg.actions.append(of.ofp_action_output(port = 5))
                                                self.connection.send(msg)
                                        #AnyHost->untrustedHost
                                        elif check_IPV4.dstip == untrustedHost_IP: #Trying to send anything to untrusted Host
                                                msg.actions.append(of.ofp_action_output(port = 5))
                                                self.connection.send(msg)
                                        #Trying to send to trustedHost from untrustedHost
                                        elif check_IPV4.srcip == untrustedHost_IP and check_IPV4.dstip == trustedHost_IP: #untrustedHost->trustedHost
                                                msg.actions.append(of.ofp_action_output(port = 4))
                                                self.connection.send(msg)
                                    	elif check_IPV4.dstip == host10_IP: #Trying to send data to Host10 #(AnyHost->Host10)
						msg.actions.append(of.ofp_action_output(port = 1))
						self.connection.send(msg)
					elif check_IPV4.dstip == host20_IP: #Trying to send data to Host20 (AnyHost->Host20)
						msg.actions.append(of.ofp_action_output(port = 2))
						self.connection.send(msg)
					elif check_IPV4.dstip == host30_IP: #Trying to send data to Host30 (AnyHost->Host30)
						msg.actions.append(of.ofp_action_output(port = 3))
						self.connection.send(msg)
					elif check_IPV4.dstip == trustedHost_IP: #Trying to send data to Trusted Host (Any->trusted)
						msg.actions.append(of.ofp_action_output(port = 4))
						self.connection.send(msg)
					elif check_IPV4.dstip == untrustedHost_IP: #Trying to send data to Untrusted Host (Any->untrusted)
						msg.actions.append(of.ofp_action_output(port = 5))
						self.connection.send(msg)
					#Trying to send data to Server from someone who is not untrustedHost
					elif check_IPV4.srcip != untrustedHost_IP and check_IPV4.dstip == server_IP: # !untrustedHost->server
						msg.actions.append(of.ofp_action_output(port = 6))
						self.connection.send(msg)
					else: #If the protocol is not defined, just block.
						print("\nBLOCK")
						#msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))
						self.connection.send(msg)

	def _handle_PacketIn (self, event):
		"""
		Handles packet in messages from the switch.
		"""
		packet = event.parsed # This is the parsed packet data.
		if not packet.parsed:
			log.warning("Ignoring incomplete packet")
			return

		packet_in = event.ofp # The actual ofp_packet_in message.
		self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
	"""
	Starts the component
	"""
	def start_switch (event):
		log.debug("Controlling %s" % (event.connection,))
		Final(event.connection)
	core.openflow.addListenerByName("ConnectionUp", start_switch)

# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

######################################################################################################
# Shawn Chumbar
# CMPE 150: Lab 3
# Professor Christina Parsa
# lab3controller.py
######################################################################################################
# Resources Used :
# http://intronetworks.cs.luc.edu/auxiliary_files/mininet/poxwiki.pdf
# https://en.wikipedia.org/wiki/EtherType
######################################################################################################

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()


class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """

  def __init__(self, connection):
	# Keep track of the connection to the switch so that we can
	# send it messages
	self.connection = connection

	# This binds our PacketIn event listener
	connection.addListeners(self)

  def do_firewall(self, packet, packet_in):
	######################################################################################################
	#						Rules:
	#1. Allow any ARP traffic.
	#2. Allow any ICMP traffic.
	#3. TCP traffic should be allowed between h1 and h3 (both h1 to h3 and h3 to h1).
	#4. Any other traffic should be dropped irrespective of the protocol.
	######################################################################################################
	# The code in here will be executed for every packet.

	# Making the table
	# Installing table entry

	msg = of.ofp_flow_mod()
	
	# match packet
	msg.match = of.ofp_match.from_packet(packet)
	
	# few entries of dump--flows from timeout
	msg.idle_timeout = 25  # 50
	msg.hard_timeout = 50  # 100
	
	isARP = packet.find('arp')
	isTCP = packet.find('tcp')
	isICMP = packet.find('icmp')

	# If we are using ARP, TCP, or ICMP
	if isICMP is not None or isARP is not None or isTCP is not None:
		# 2.Allow any ICMP traffic
		if isICMP is not None:
		# accept packet
			msg.data = packet_in
			msg.nw_proto = 6 #6=tcp
			# add action to send to specified port
			action = of.ofp_action_output(port = of.OFPP_FLOOD)
			msg.actions.append(action)
			self.connection.send(msg)

		#1. Allow any ARP traffic
		elif isARP is not None:
		# accept packet
			msg.data = packet_in
			msg.match.dl_type = 0x0806  # match ARP
			# add action to send to specified port
			action = of.ofp_action_output(port=of.OFPP_FLOOD)
			msg.actions.append(action)
			self.connection.send(msg)

		# 3. TCP traffic should be allowed between h1 and h3 (both h1 to h3 and h3 to h1). 
		elif isTCP is not None:
		# accept packet
			isIPV4 = packet.find('ipv4')
			if (isIPV4.srcip == '10.0.1.10' and isIPV4.dstip == '10.0.1.30') or (isIPV4.srcip == '10.0.1.30' and isIPV4.dstip == '10.0.1.10'):
				msg.data = packet_in
				msg.nw_proto = 6 # 6 = tcp
				# add action to send to specified port
				action = of.ofp_action_output(port = of.OFPP_FLOOD)
				msg.actions.append(action)
				self.connection.send(msg)
		else:
			# no packets taken - packet dropped
			# msg.data = packet_in
			self.connection.send(msg)

	#4. Any other traffic should be dropped irrespective of the protocol.
	else:
	#	# msg.data = packet_in
		self.connection.send(msg)

	###################################################

  def _handle_PacketIn (self, event):
	"""
	Handles packet in messages from the switch.
	"""

	packet = event.parsed # This is the parsed packet data.
	if not packet.parsed:
	  log.warning("Ignoring incomplete packet")
	  return

	packet_in = event.ofp # The actual ofp_packet_in message.
	self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
	log.debug("Controlling %s" % (event.connection,))
	Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
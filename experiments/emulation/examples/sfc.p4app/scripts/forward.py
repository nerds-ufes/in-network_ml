#!/usr/bin/python

import socket
import struct

rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
s.bind(("eth0", socket.htons(0x0800)))

while True:
    receivedPacket = rawSocket.recv(2048)
    ipHeader = receivedPacket[14:34]
    ipHdr = struct.unpack("!12s4s4s", ipHeader)
    destinationIP = socket.inet_ntoa(ipHdr[2])
    sourceIP = socket.inet_ntoa(ipHdr[1])
    if sourceIP == "10.0.1.1" or destinationIP == "10.0.1.1":
		s.send(receivedPacket)

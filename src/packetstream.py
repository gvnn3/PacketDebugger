# Copyright (c) 2007, Neville-Neil Consulting
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# Neither the name of Neville-Neil Consulting nor the names of its 
# contributors may be used to endorse or promote products derived from 
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# File: packet_stream.py
#
# Author: George V. Neville-Neil
#
# Description: This module implements operations on streams of packets
# for the packet debugger.  The user interacts with streams in order
# to read, write and manipulate packets.

import pcs
import pcap

class InitError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class Stream(object):
    """A class which represents a stream of packets for PDB
    """

    def __init__(self, options, filename=None, interface=None):
        """Initialize a packet stream.

        A packet stream can be read from a pcap file or it can be
        taken live from an interface.  Either or, but not both, must
        be supplied.  A pcap dump file is read in completely once it
        is opened and is then available to the system."""

        # Set up all known data in a common place
        self.breakpoints = [] # List of integer breakpoints
        self.file = None      # The file we are working with.
        self.filter = ""      # Pcap style filter
        self.packets = []     # The list of packets
        self.position = -1    # Where we are in the list of packets
        self.type = None      # What type of stream this is XXX
        self.lock = None      # A lock for use in threading XXX
        self.layer = 0        # The ISO layer we're working with.

        if filename == None and interface == None:
            raise InitError, "Must supply a file or an interface"
        if filename != None and interface != None:
            raise InitError, "Cannot supply both a file AND an interface"
        self.options = options

        if (interface != None):
            raise InitError, "Live capture not supported"

        if (filename != None):
            try:
                self.file = pcs.PcapConnector(filename)
            except:
                raise InitError, "Cannot open pcap file %s" % filename
            
            done = False
            packet = None
            while not done:
                try:
                    packet = self.file.readpkt()
                except:
                    done = True
                
                self.packets.append(packet)
# XXX FIX PCS                self.file.close()
            self.position = 0

            if self.file.dlink == pcap.DLT_EN10MB:
                layer = 2
            else:         # Default case
                layer = 3 # Network and above

    def __str__(self):
        retval = ""
        retval += "Breakpoints\n"
        retval += "File\n"
        retval += "Filter\n"
        retval += "Number of packets: %d\n" % len(self.packets)
        retval += "Current Position: %d\n" % self.position
        retval += "Type\n"
        retval += "Layer: %d" % self.layer
        return retval

    def __repr__(self):
        return "<pdb.Stream bp, file, filter, numpkts %d, position %d, type, layer %d>" % (len(self.packets), self.position, self.layer)

    def run(self):
        pass

    def list(self):
        """List the packets in the stream."""
        if (self.position + self.options.list_length) > len(self.packets):
            end = len(self.packets)
        else:
            end = self.position + self.options.list_length
        
        index = self.position
        for packet in self.packets[self.position:end]:
            self.display(index, packet)
            print
            index+=1

    def display(self, index, packet):
        """Method for displaying packets."""
        if packet == None:
            print "%d: Unknown Packet"
            return
        if (self.options.layer == -1):
            print "%d: %s" % (index, packet.println())
            while True:
                try:
                    packet = packet.data
                except:
                    return
                if (packet == None):
                    return
                print "  %s" % packet.println()
        else:
            if self.options.layer < self.layer:
                return
            if self.options.layer == self.layer:
                print "%d: %s" % (index, packet.println())
                return
            skip = self.options.layer - self.layer
            while skip > 0:
                try:
                    packet = packet.data 
                except:
                    return
                skip-= 1
                if (packet == None):
                    return
            print "%d: %s" % (index, packet.println())

    def next(self, arg):
        """Move to the next packet"""
        jump = 1
        if (arg != None):
            jump = int(arg)
        if ((self.position + jump) > len(self.packets)):
            print "Distance %d is too far" % jump
            return 
        self.position += jump

    def prev(self, arg):
        """Move to the previous packet."""
        jump = 1
        if (arg != None):
            jump = int(arg)
        if (self.position <= 0):
            print "Distance %d is too far" % jump
            return
        self.position -= jump


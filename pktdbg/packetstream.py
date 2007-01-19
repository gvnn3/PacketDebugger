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

        self.options = options

        if (interface != None):
            try:
                self.outfile = pcs.PcapConnector(interface)
            except:
                raise InitError, "Cannot open interface %s, you may need to be root." % interface

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

            self.file.close()
            self.position = 0

            if (self.file.dlink == pcap.DLT_EN10MB):
                self.layer = 2
            else:         # Default case
                self.layer = 3 # Network and above

    def __str__(self):
        """give a human readable version of a Stream"""
        retval = ""
        retval += "Breakpoints %s\n" % self.breakpoints
        retval += "File %s\n" % self.file.file.name
        retval += "Filter %s\n" % self.file.file.filter
        retval += "Number of packets: %d\n" % len(self.packets)
        retval += "Current Position: %d\n" % self.position
        retval += "Type\n"
        retval += "Layer: %d\n" % self.layer
        if self.file.dlink == pcap.DLT_NULL:
            datalink = "Localhost"
        elif self.file.dlink == pcap.DLT_EN10MB:
            datalink = "Ethernet"
        else:
            datalink = "Unknown"
        retval += "Datalink: %s\tOffset: %d" % (datalink, self.file.dloff)
        return retval

    def __repr__(self):
        return "<pdb.Stream bp, file, filter, numpkts %d, position %d, type, layer %d>" % (len(self.packets), self.position, self.layer)

    def run(self, index, ignore = -1):
        """Run the packet stream from the index.  If ignore is set the ignore the breakpoint at that numbered index"""
        if ((self.file.dlink != self.outfile.dlink) and (self.outfile.dlink != pcap.DLT_NULL)):
            print "Input stream and output interface must agree."
            print "Input stream dlink %d, output interface dlink %d" % (self.file.dlink, self.outfile.dlink)
            print "run stopped"
            return

        self.position = index
        for packet in self.packets[index:len(self.packets)]:
            if ((self.position in self.breakpoints) and
                (self.position != ignore)):
                print "Breakpoint at packet %d" % self.position
                self.display(self.position, packet)
                return
            packet = self.map(packet, self.outfile)
            try:
                written = self.outfile.write(packet.bytes, len(packet.bytes))
            except:
                print "Writing packet %d failed, aborting." % self.position
                return
            self.position += 1

    def send(self, packet):
        """Send a single packet"""
        packet = self.map(packet, self.outfile)
        try:
            written = self.outfile.write(packet.bytes, len(packet.bytes))
        except:
            print "Sending packet failed."
            return

    def map(self, packet, device):
        """Take a packet and make it transmittable on the device passed in."""
        if (self.file.dloff == device.dloff):
            return packet.chain()

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

    def update(self, packet):
        "Interactively update a packet."
        pass

    def next(self, jump=1):
        """Move to the next packet"""
        if ((self.position + jump) > len(self.packets)):
            print "Distance %d is too far" % jump
            return 
        self.position += jump
        self.display(self.position, self.packets[self.position])

    def prev(self, jump=1):
        """Move to the previous packet."""
        if (self.position <= 0):
            print "Distance %d is too far" % jump
            return
        if ((self.position - jump) < 0):
            print "Distance %d is too far" % jump
            return
        self.position -= jump
        self.display(self.position, self.packets[self.position])

    def add_break(self, arg):
        """Add a breakpoint."""
        if (arg < 0 or arg > len(self.packets)):
            print "Cannot set breakpoint at packet %d" % arg
            return
        if (arg in self.breakpoints):
            print "Breakpoint already set at %d" % arg
            return
        self.breakpoints.append(arg)
        self.breakpoints.sort()
        
    def del_break(self, arg):
        if (arg < 0 or arg > len(self.packets)):
            print "No breakpoint set at packet %d" % arg
            return
        self.breakpoints.remove(arg)

    def clear_break(self):
        self.breakpoints = []
    

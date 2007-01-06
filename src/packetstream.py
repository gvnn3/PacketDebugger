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

from pcs import *

class InitError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class Stream(object):

    # Per stream data

    breakpoints = () # a list of integers which are breakpoints for the stream
    file = None        # The file or device we are working with.
    filter = ""      # A filter passed into the pcap/bpf system for
                     # filtering the packets we receive
    packets = None   # The packets we are examining.
    position = -1    # Our current location in the packet array/stream
    type = None      # Either Capture or a Playback stream.
    lock = None # A lock for use by threading code (not used yet)
    options = None   # The options 

    def __init__(self, options, filename=None, interface=None):
        """Initialize a packet stream.

        A packet stream can be read from a pcap file or it can be
        taken live from an interface.  Either or, but not both, must
        be supplied.  A pcap dump file is read in completely once it
        is opened and is then available to the system."""

        if filename == None && interface == None:
            raise InitError, "Must supply a file or an interface"
        if filename != None && interface != None:
            raise InitError, "Cannot supply both a file AND an interface"
        options = options

        if (interface != None):
            raise InitError, "Live capture not supported"

        if (filename != None):
            try:
                self.file = pcs.PcapConnector(filename)
            except:
                raise InitError, "Cannot open pcap file %s" % filename
            
        while not done:
            try:
                packet = self.file.read()
            except:
                done = True
            self.packets.append(packet)

        self.file.close()
        self.position = 0

    def run(self):
        pass

    def list(self):
        """List the packets in the stream."""
        if (self.position + options.list_length) > len(self.packets):
            end = len(self.packets)
        else:
            end = self.position + options.list_length
        
        for packet in self.packets[self.position:end]:
            display(packet)

    def display(self, packet):
        """Method for displaying packets."""
        print packet
    

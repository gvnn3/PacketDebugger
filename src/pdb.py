#!/usr/bin/env python
#
# Copyright (c) 2006, Neville-Neil Consulting
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
# File: pdb.py
#
# Author: George V. Neville-Neil
#
# Description: This is the script which starts up the Packet Debugger.
# It is installed, along with all of its supporting modules, when the
# system is installed.

import sys
import cmd  # Used to implement our CLI

sys.path.insert(0, ".") # Look locally first.
# Import all of the datatypes we need for the debugger.
import packetstream

streams = []  # The list of streams we're working with.
current = None   # The current stream number
options = None  # Global pointer to all options for the program

class Options(object):

    list_length = 10 # How many lines to list before and after this one.
    layer = -1     # Pick a layer to display, None is all layers

    def __init__(self):
        pass

    def __repr__(self):
        return "list_length = %d\nlayer = %d\n" % (self.list_length, self.layer)

def main():
    """The Packet Debugger

    The packet debugger is a program that treats network packets, in
    the form of either live captured packets or packets read from a
    file stored using the standard pcap(3) library as statements which
    can be worked with in much the same way that a code debugger works
    with lines of code.

    """

    # Standard argument parsing with the optparse module.
    # Currently there are no positional arguments with pdb.
    
    from optparse import OptionParser 
    parser = OptionParser() 

    parser.add_option("-f", "--file", dest="filename", 
                      help="pcap file to read") 
    parser.add_option("-i", "--interface", dest="interface",
                      help="Network interface to connect to.")

    (cmdln_options, args) = parser.parse_args() 
    
    global options
    options = Options()

    # Read in stream 0
    streams.append(packetstream.Stream(options, cmdln_options.filename))
    global current
    current = streams[0]
    
    # Jump into the cli

    cli = Command()

    cli.cmdloop()
    
class Command(cmd.Cmd):
    """The Command Line Interpreter for the packet debugger.

    This class uses the built in command interpreter from Python to
    build up the full set of commands implemented by the debugger.
    Each command is written as a do_xxx function in this class

    Each command takes a string which should be parsed as arguments.

    Help follows the command."""

    global current
    
    def do_quit(self, message):
        print "Bye"
        sys.exit()

    def help_quit(self):
        print "Bye"
        sys.exit()

    def do_create(self, args):
        """Create a new stream from a file or network interface.

        Acceptable argument lists are:
        file filename
        interface interfacename
        """
        global current
        try:
            arg_list = args.split()
        except:
            self.help_create()
            return
        if (len(arg_list) != 2):
            self.help_create()
            return
        current.list()
        print current
        current = packetstream.Stream(options, arg_list[1])
        print current
        current.list()
        streams.append(current)
        
    def help_create(self):
        print "create file|interface filename|interface name"
        print "Create a new stream from a file or a network interface."
        
    def do_delete(self, args):
        print "delete stream"

    def help_delete(self):
        print "delete stream"

    def do_run(self, args):
        print "run stream"

    def help_run(self):
        print "run stream"

    def do_list(self, args):
        print current
        current.list()

    def help_list(self):
        print "list packets"

    def do_print(self, args):
        print "print packet"

    def help_print(self,):
        print "print packet"

    def do_send(self, args):
        print "send packet"

    def help_send(self):
        print "send packet"

    def do_set(self, args):
        global current
        if len(args) <= 0:
            self.help_set()
            return
        try:
            (key, value) = args.split()
        except:
            self.help_set()

        if key == "list_length":
            options.list_length = int(value)
        elif key == "layer":
            value = int(value)
            if value < 0:
                options.layer = None
            if value > 7:
                self.help_set()
            else:
                options.layer = value
        elif key == "current":
            value = int(value)
            if value < 0:
                print "Must be greater than 0"
                self.help_set()
                return
            if value >= len(streams):
                print "Must be less than %d" % (len(streams) - 1)
                self.help_set()
                return
            else:
                current = streams[value]
        
    def help_set(self):
        print "set option value\n\noptions: list_length - how many packets to list at one time.\n         layer - ISO layer to show, -1 shows all\n         current - set the current stream we're inspecting [0..n]"

    def do_show(self, args):
        """Show the current options that are set."""
        print options

    def do_break(self, args):
        print "set breakpoint"

    def help_break(self):
        print "set breakpoint"

    def do_continue(self, args):
        print "continue"

    def help_continue(self):
        print "continue"

    def do_next(self, args):
        """Move to the next packet"""
        if (len(args) > 0):
            if (type(args) != str):
                print "N must be a number"
                self.help_next()
                return
            if (args.isdigit() != True):
                print "N must be a number"
                self.help_next()
                return
            current.next(args)
        else:
            current.next(None)

    def help_next(self):
        print "next (N)"
        print "Move to the next packet in the list.  With a numeric argument, N, move N packets ahead in the list."

    def do_prev(self, args):
        """Move to the previous packet"""
        if (len(args) > 0):
            if (type(args) != str):
                print "N must be a number"
                self.help_next()
                return
            if (args.isdigit() != True):
                print "N must be a number"
                self.help_next()
                return
            current.prev(args)
        else:
            current.prev(None)

    def help_prev(self):
        print "prev (N)"
        print "Move to the previous packet in the list.  With a numeric argument, N, move N packets back in the list."

    def do_info(self, args):
        print "Stream %d" % streams.index(current)
        print "---------"
        print current

    def help_info(self):
        print "Print out all the information on the current stream."


# The canonical way to start a Python script.  Keep at the end.
if __name__ == "__main__":
    main()


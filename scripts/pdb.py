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

# Import all of the datatypes we need for the debugger.
from pdb import *

streams = []  # The list of streams we're working with.

class Options(object):

    list_length = 10 # How many lines to list before and after this one.

    def __init__(self):
        pass

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

    (options, args) = parser.parse_args() 
    


    user_opts = Options()

    # Jump into the cli

    cli = Command()

    cli.cmdloop()
    
class Command(cmd.Cmd):
    """The Command Line Interpreter for the packet debugger.

    This class uses the built in command interpreter from Python to
    build up the full set of commands implemented by the debugger.
    Each command is written as a do_xxx function in this class"""

    def do_quit(self, message):
        print "Bye"
        sys.exit()

    def do_create(self, args):
        print "create stream"

    def do_delete(self, args):
        print "delete stream"

    def do_run(self, args):
        print "run stream"

    def do_list(self, args):
        print "list packets"

    def do_print(self, args):
        print "print packet"

    def do_send(self, args):
        print "send packet"

    def do_set(self, args):
        print "set"

    def do_break(self, args):
        print "set breakpoint"

    def do_continue(self, args):
        print "continue"

    def do_next(self, args):
        print "next"

    def do_prev(self, args):
        print "prev"

    def do_info(self, args):
        print "info"


# The canonical way to start a Python script.  Keep at the end.
if __name__ == "__main__":
    main()


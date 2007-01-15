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
# File: $Id: $
#
# Author: George V. Neville-Neil
#
# Description: This module contains all the code which implementes the
# CLI for the Packet Debugger

import sys
import cmd  # Used to implement our CLI
import packetstream

class Command(cmd.Cmd):
    """The top level  Command Line Interpreter for the packet debugger.

    This class uses the built in command interpreter from Python to
    build up the full set of commands implemented by the debugger.
    Each command is written as a do_xxx function in this class

    Each command takes a string which should be parsed as arguments.

    Help follows the command."""

    def __init__(self, current, options, streams):
        self.current = current
        self.options = options
        self.streams = streams
        self.prompt = "pdb> "
        cmd.Cmd.__init__(self)

    def do_quit(self, message):
        print "Bye"
        sys.exit()

    def help_quit(self):
        print "Quit the debugger"

    def do_create(self, args):
        """Create a new stream from a file or network interface.

        Acceptable argument lists are:
        file filename
        interface interfacename
        """
        try:
            arg_list = args.split()
        except:
            self.help_create()
            return
        if (len(arg_list) != 2):
            self.help_create()
            return

        self.current = packetstream.Stream(self.options, arg_list[1])
        self.streams.append(self.current)

    def help_create(self):
        print "create file|interface filename|interface name"
        print "Create a new stream from a file or a network interface."
        
    def do_delete(self, args):
        """Delete a stream.  If N is present delete that stream."""
        if ((self.current == None) or (len(self.streams) <= 0)):
            print "No streams.  Use the create command to create one."
            return
        if (args == ""):
            self.streams.remove(self.current)
            if (len(self.streams) > 0):
                self.current = self.streams[0]
            else:
                self.current = None
        else:
            index = self.numarg(args)
            if (index == None):
                help_delete()
                return
            else:
                if (self.streams[index] == self.current):
                    self.current = None
                del self.streams[index]
                if (len(self.streams) > 0):
                    self.current = self.streams[0]
                
            
    def help_delete(self):
        print "delete (N)"
        print "Delete a Stream.  If N is given delete a specific stream otherwise delete the current one."

    def do_run(self, args):
        """Run the current stream or the one given in the index."""
        if (args == ""):
            if (self.current != None):
                self.current.run(0)
            else:
                print "No current stream.  Use the create or set commands"
        else:
            numarg = self.numarg(args)
            if (numarg == None):
                self.help_run()
                return
            if ((numarg < 0) or (numarg >= len(self.streams))):
                print "Stream must be between 0 and %d." % (len(self.streams) - 1)
                self.help_run(0)
                return
            self.streams[numarg].run(0)

    def help_run(self):
        print "run (N)"
        print "run the current stream or the stream given by the index"

    def complete_run(self, text, line, begidx, endidx):
        stream_list = []
        for i in range(0, len(self.streams)):
            stream_list.append(str(i))
        return stream_list

    def do_continue(self, args):
        """Continue the current stream or the one given in the index."""
        if (args == ""):
            if (self.current != None):
                self.current.next()
                self.current.run(self.current.position)
            else:
                print "No current stream.  Use the create or set commands"
        else:
            numarg = self.numarg(args)
            if (numarg == None):
                self.help_run()
                return
            if ((numarg < 0) or (numarg >= len(self.streams))):
                print "Stream must be between 0 and %d." % (len(self.streams) - 1)
                self.help_run()
                return
            self.streams[numarg].next()
            self.streams[numarg].run(self.streams[numarg].position)

    def help_continue(self):
        print "continue (N)"
        print "continue the current stream or the stream given by the index"

    def do_list(self, args):
        if (args == ""):
            if (self.current != None):
                self.current.list()
            else:
                print "No current stream.  Use the create or set commands"
        else:
            numarg = self.numarg(args)
            if (numarg == None):
                self.help_list()
                return
            if ((numarg < 0) or (numarg >= len(self.streams))):
                print "Stream must be between 0 and %d." % (len(self.streams) - 1)
                self.help_list()
                return
            self.streams[numarg].list()

    def help_list(self):
        print "list (N)"
        print "list packets from current stream or the stream at index N "

    def complete_list(self, text, line, begidx, endidx):
        stream_list = []
        for i in range(0, len(self.streams)):
            stream_list.append(str(i))
        return stream_list

    def do_print(self, args):
        if (args == ""):
            if (self.current == None):
                print "No current stream.  Use the create or set commands"
                return
            else:
                numarg = self.current.position
        else:
            numarg = self.numarg(args)
            if (numarg == None):
                self.help_print()
                return
        if ((numarg < 0) or (numarg > (len(self.current.packets) - 1))):
            print "Index must be between 0 and %d." % (len(self.current.packets) - 1)
            return
        
        self.current.display(numarg, self.current.packets[numarg])

    def help_print(self):
        print "print (N)"
        print "print the current packet in the current stream or packet N in the current stream"

    def do_send(self, args):
        print "send packet"

    def help_send(self):
        print "send packet"

    def do_set(self, args):
        if len(args) <= 0:
            self.help_set()
            return
        try:
            (key, value) = args.split()
        except:
            self.help_set()
            return

        if key == "list_length":
            self.options.list_length = int(value)
        elif key == "layer":
            value = int(value)
            if value < 0:
                self.options.layer = None
            if value > 7:
                self.help_set()
            else:
                self.options.layer = value
        elif key == "current":
            if (value == None):
                print "Must supply a number between 0 and %d" % len(self.streams - 1)
                self.help_set()
                return
            value = int(value)
            if value < 0:
                print "Must be greater than 0"
                self.help_set()
                return
            if value >= len(self.streams):
                print "Must be less than %d" % (len(self.streams) - 1)
                self.help_set()
                return
            else:
                self.current = self.streams[value]
        
    def complete_set(self, text, line, begidx, endidx):
        """Completion for the set command"""
        if (text in ["li", "lis", "list", "list_", "list_l", "list_le", "list_len", "list_leng", "list_lengt"]):
            return ["list_length"]
        elif (text in ["la", "lay", "laye"]):
            return ["layer"]
        elif (text in ["c", "cu", "cur", "curr", "curre", "curren"]):
            return ["current"]
        else:
            if (line == "set current "):
                stream_list = []
                for i in range(0, len(self.streams)):
                    stream_list.append(str(i))
                return stream_list
              
    def help_set(self):
        print "set option value\n\noptions: list_length - how many packets to list at one time.\n         layer - ISO layer to show, -1 shows all\n         current - set the current stream we're inspecting [0..n]"

    def do_show(self, args):
        """Show the current options that are set."""
        print self.options

    def do_break(self, args):
        """set a breakpoint at the current index in the stream or at the numeric index given"""
        if (args == ""):
            numarg = self.current.position
        else:
            numarg = self.numarg(args)
        if (numarg == None):
            self.help_break()
            return
        self.current.add_break(numarg)

    def help_break(self):
        print "break (N)"
        print "set a breakpoint at the current index in the stream or at the numeric index given"

    def do_next(self, args):
        """Move to the next packet"""
        if (self.current == None):
            print "No current stream.  Use the create or set commands"
            return
        if (len(args) > 0):
            jump = self.numarg(args)
            if (jump == None):
                self.help_next()
                return
            else:
                self.current.next(jump)
        else:
            self.current.next()

    def help_next(self):
        print "next (N)"
        print "Move to the next packet in the list.  With a numeric argument, N, move N packets ahead in the list."

    def do_prev(self, args):
        """Move to the previous packet"""
        if (self.current == None):
            print "No current stream.  Use the create or set commands"
            return
        if (len(args) > 0):
            jump = self.numarg(args)
            if (jump == None):
                self.help_prev()
                return
            else:
                self.current.prev(jump)
        else:
            self.current.prev()

    def help_prev(self):
        print "prev (N)"
        print "Move to the previous packet in the list.  With a numeric argument, N, move N packets back in the list."

    def do_info(self, args):
        if (len (args) <= 0):
            if (self.current == None):
                print "No current stream.  Use the create or set commands"
                return
            print "Stream %d" % self.streams.index(self.current)
            print "---------"
            print self.current
        else:
            arg_list = args.split()
            if (arg_list[0] == "all"):
                for stream in self.streams:
                    print "Stream %d" % self.streams.index(stream)
                    print "---------"
                    print stream
            elif (arg_list[0] == "break"):
                print "Stream %d breakpoints %s" % (self.streams.index(self.current), self.current.breakpoints)
            elif (arg_list[0].isdigit() == True):
                index = int(arg_list[0])
                try:
                    stream = self.streams[index]
                except:
                    print "No stream %d" % index
                    return
                print "Stream %d" % index
                print "---------"
                print self.streams[index]
            else:
                self.help_info()
                return
            
    def complete_info(self, text, line, begidx, endidx):
        """Completion of the arguments for the info command"""
        if (text in ["a" , "al", "all"]):
            return ["all"]
        elif (text in ["b", "br", "bre", "brea"]):
            return ["break"]
        else:
            stream_list = []
            for i in range(0, len(self.streams)):
                stream_list.append(str(i))
            return stream_list

    def help_info(self):
        print "info [N | all]"
        print "Print out all the information on the current stream, a specific stream (N), or all streams."

    def numarg(self, args):
        """If the argument passed is numeric pass back the number, otherwise pass back None"""
        if (type(args) != str):
            print "N must be a number"
            return None
        if (args.isdigit() != True):
            print "N must be a number"
            return None
        return int(args)


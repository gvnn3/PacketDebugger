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
# Description: This module implements network time diagrams by
# interfacing to the graphviz package using the pydot module.  If
# pydot is not installed this module will fail gracefully.

from pydot import *

def graph(packets, layer=1):
    """output a graph of the packets using data from layer to determine the source and destination"""
    sources = {}
    destinations = {}
    
    #         srcname = pcs.source(packets[0])
    #         dstname = pcs.destination(packets[0])
    srcname = "src"
    dstname = "dst"
    index = 0
    prevsrc = ""
    prevdst = ""
    graph = Dot(simplify=True, prog = 'dot', type='digraph')
    graph.add_node(Node("Start"))
    first = True
    for packet in packets:
        if not hasattr(packet, srcname):
            print "cannot determing packet source, skipping"
            continue
        if not hasattr(packet, dstname):
            print "cannot determing packet destination, skipping"
            continue
        
        src = packet.pretty(srcname)
        dst = packet.pretty(dstname)
        
        src = src.replace(":", "&#58;")
        dst = dst.replace(":", "&#58;")

        snode = repr(index) + " " + src
        dnode = repr(index) + " " + dst

        if src not in sources:
            sources[src] = Subgraph(index)
            sources[src].label = "Source"
        else:
            edge = Edge(snode, dnode)
            edge.label = packet.println()
            graph.add_edge(edge)
            
        if dst not in destinations:
            destinations[dst] = Cluster("Destination")
            destinations[dst].label = "Destination"
        else:
            edge = Edge(dnode, snode)
            edge.label = packet.println()
            graph.add_edge(edge)
            
        if first == True:
            graph.add_edge(Edge("Start", snode))
            graph.add_edge(Edge("Start", dnode))
            first = False
            
        if prevsrc != "":
            sources[src].add_edge(Edge(prevsrc, snode))
        if prevdst != "":
           destinations[dst].add_edge(Edge(prevdst, dnode))
        
        prevsrc = snode
        prevdst = dnode

        index += 1

    for subgraph in sources.values():
         graph.add_subgraph(subgraph)
    for subgraph in destinations.values():
         graph.add_subgraph(subgraph)

    graph.write_gif("graph.gif", prog="dot")
    graph.write_raw("graph.dot", prog="dot")

#
# File: $Id:$
#
# Author: George V. Neville-Neil
#
# Documentation Makefile for the Packet Debugger.  You can build
# various versions of the docs from here.

.SUFFIXES: .tex .pdf

SRCS= pdb.tex

all: ${SRCS:S/.tex/.pdf/}

.tex.pdf:
	pdflatex ${.IMPSRC}

clean::
	rm -rf *.pdf *.html *.out *.log
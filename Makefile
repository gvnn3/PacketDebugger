#
#
# File: $Id:$
#
# Author: George V. Neville-Neil
#
# Makefile for building distributions of the Packet Debugger.  
install::
	python setup.py install

dist::
	python setup.py sdist

clean::
	rm -rf dist build MANIFEST
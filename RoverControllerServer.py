#!/usr/bin/env python

'''
@author: Dominic Baratta <dbaratta@buffalo.edu>

This source files contains a control server capable of basic "remote control"
of a ground platform via a TCP/IP tunnel.

WARNING: This source code has not been throughly tested. It should not be used
where it would create danger to property / life (e.g. remote controlled 
quad-rotors, large ground vehicles, robotic lawn mowers, etc).

Copyright (c) 2013, Dominic Baratta All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 
3. The name of Dominic Baratta may not be used to endorse or promote
   products derived from this software without specific prior written permission

THIS SOFTWARE IS PROVIDED BY DOMINIC BARATTA "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE EXPRESSLY AND
SPECIFICALLY DISCLAIMED. IN NO EVENT SHALL DOMININC BARATTA BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import serial   # PySerial library
import socket   # Python TCP/IP library

print "Starting the Rover Server"

# Open a serial connection on /dev/ttyS0 at 9600 baud with 8 data
# bits and 1 stop bit
ser = serial.Serial("COM21", 9600)

TCP_IP = '127.0.0.1'    # 'localhost'
TCP_PORT = 5005         # Port to listen on
BUFFER_SIZE = 1024      # Message buffer size

# Wait for a connection on the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

s.listen(1)

while 1:
  conn, addr = s.accept()
  print 'Client Connected! Address:', addr
  
  while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print 'Received: ', data
    ser.write(data)
  conn.close()

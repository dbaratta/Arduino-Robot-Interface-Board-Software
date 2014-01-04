#!/usr/bin/env python

'''
@author: Dominic Baratta <dbaratta@buffalo.edu>

This source files contains a control server capable of basic "remote control"
of a ground platform via a TCP/IP tunnel.

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

import socket # Python TCP/IP socket library
import pygame # Pygame library. (Used for GUI + keyboard input)
import time   # Python time library


TCP_IP = '127.0.0.1'      # IP Address of the platform
TCP_PORT = 5005           # Port to connect to the platform on
BUFFER_SIZE = 1024        # Message buffer size (this should be fine)

black = 0, 0, 0           # Pygame Window background color
is_running = 1            # Control app keep alive variable (set to 0 to kill)

default_speed = 100
mult = 0.5

# Variable initialization
m1_speed = 0
m2_speed = 0
up_arrow = 0
down_arrow = 0
left_arrow = 0
right_arrow = 0

# Init PyGame (for the GUI)
pygame.init()
size = width, height = 320, 240

# Create pygame window
screen = pygame.display.set_mode(size)

# Fill in the background as black
screen.fill(black)

# "Flip" the display
pygame.display.flip()

# Configure PyGame to generate keydown interrupts every half a second for keys
# which are held down
pygame.key.set_repeat(1, 1000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# Loop until the user hits the "escape" key
while is_running:  
  events = pygame.event.get() # Grab the keyboard state (pressed keys)
  for event in events:  # Loop through all the keys
    if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
      # User hit the escape key. Exit control application
      is_running = 0  # Set flag to exit application
    
    if ((event.type == pygame.KEYDOWN) and 
        ((event.key == pygame.K_UP) or (event.key == pygame.K_w))):
      # User has either the Up arrow or the 'w' key pressed
      up_arrow = 1
    elif ((event.type == pygame.KEYUP) and
          ((event.key == pygame.K_UP) or (event.key == pygame.K_w))):
      # User has either the Up arrow or the 'w' key released
      up_arrow = 0
        
    if ((event.type == pygame.KEYDOWN) and 
        ((event.key == pygame.K_DOWN) or (event.key == pygame.K_s))):
      # User has either the Down arrow or the 's' key pressed
      down_arrow = 1
    elif ((event.type == pygame.KEYUP) and 
        ((event.key == pygame.K_DOWN) or (event.key == pygame.K_s))):
      # User has either the Down arrow or the 's' key released
      down_arrow = 0
      
    if ((event.type == pygame.KEYDOWN) and 
        ((event.key == pygame.K_LEFT) or (event.key == pygame.K_a))):
      # User has either the Left arrow or the 'a' key pressed
      left_arrow = 1
    elif ((event.type == pygame.KEYUP) and
          ((event.key == pygame.K_LEFT) or (event.key == pygame.K_a))):
      # User has either the Left arrow or the 'a' key released
      left_arrow = 0
        
    if ((event.type == pygame.KEYDOWN) and 
        ((event.key == pygame.K_RIGHT) or (event.key == pygame.K_d))):
      # User has either the Right arrow or the 'd' key pressed
      right_arrow = 1
    elif ((event.type == pygame.KEYUP) and
          ((event.key == pygame.K_RIGHT) or (pygame.K_d))):
      # User has either the Right arrow or the 'd' key released
      right_arrow = 0
        
    if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_p)):
      # User has the 'p' key pressed
      if(mult < 0.9): # Check if increasing the speed will result in a value > 1
        mult = mult + 0.1 # It won't. Increase speed
      
    if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_l)):
      # User has the 'l' key pressed
      if(mult > 0.2): # Check if decreasing speed will result in a value < 0.1
        mult = mult - 0.1 # It won't. Decrease speed
        
  # Processed currently pressed direction buttons
  if(up_arrow and left_arrow):
    # Arcing turn to the left while going forward
    m1_speed = default_speed * mult
    m2_speed = default_speed * (mult / 2)
    
  elif(down_arrow and left_arrow):
    # Arcing turn to the left while going backwards
    m1_speed = -(default_speed * mult)
    m2_speed = -(default_speed * (mult / 2))
    
  elif(up_arrow and right_arrow):
    # Arcing turn to the right while going forward
    m1_speed = default_speed * (mult / 2)
    m2_speed = default_speed * mult
    
  elif(down_arrow and right_arrow):
    # Arcing turn to the right while going backwards
    m1_speed = -(default_speed * (mult / 2))
    m2_speed = -(default_speed * mult)
    
  elif(up_arrow):
    # Drive forward
    m1_speed = default_speed * mult
    m2_speed = default_speed * mult
    
  elif(down_arrow):
    # Drive backward
    m1_speed = -(default_speed * mult)
    m2_speed = -(default_speed * mult)
    
  elif(left_arrow):
    # Turn to the left
    m1_speed = default_speed * mult
    m2_speed = -(default_speed * mult)
    
  elif(right_arrow):
    # Turn to the right
    m1_speed = -(default_speed * mult)
    m2_speed = default_speed * mult
  else:
    # Stopped
    m1_speed = 0
    m2_speed = 0
    
  # Build the message to the platform
  message = "M1"  # Address 'Motor 1'
  if(m1_speed >= 0):  # Positive speed
    message = message + "+"
  else:               # Negative speed
    message = message + "-"
    
  # Append motor speed from 0 - 100. Add on leading zero's
  message = message + str(abs(int(m1_speed))).zfill(3)

  message = message + " M2" # Address 'Motor 2'
  if(m2_speed >= 0):        # Positive speed
    message = message + "+"
  else:                     # Negative speed
    message = message + "-"
  
  # Append motor speed from 0 - 100. Add on leading zero's  
  message = message + str(abs(int(m2_speed))).zfill(3)
  message = message + '\n'
  
  s.send(message) # Send motor command over socket connection
  
  time.sleep(0.25)  # Sleep for 1/4 of a second

message = "M1+000 M2+000" # Control app exiting. Send a stop command
s.send(message)           # Send the stop message to the platform
s.close()                 # Close the socket connection
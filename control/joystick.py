#!/usr/bin/python           # This is server.py file

# import pygame
# 
# pygame.joystick.init()
# joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
# print joysticks
 
import socket               # Import socket module
 
s = socket.socket()         # Create a socket object
# host = socket.gethostname() # Get local machine name
host = 'pats-oci.local'
# host = '192.168.1.139'
port = 5000                # Reserve a port for your service.
 
print 'Connecting to %s:%s' % (host, port)
s.connect((host, port))
 
while True:
    msg = raw_input('CLIENT >> ')
    s.send(msg)
    msg = s.recv(1024)
    print 'SERVER >> ', msg
#s.close                     # Close the socket when done
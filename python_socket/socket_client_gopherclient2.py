#!/usr/bin/python
#Filename: socket_client_gopherclient.py

import socket,os,sys

port = 70
host = sys.argv[1]
filename = sys.argv[2]
print 'socket_OK'

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host, port))
except socket.gaierror,e:
    print 'Error connection to server: %s' %e
    sys.exit(1)
	
s.sendall(filename)

while 1:
    buf = s.recv(2048)
    if not len(buf):
        break
    sys.stdout.write(buf)

#!/usr/bin/python
#Filename: socket_client10086.py

import socket,sys
port = 70
host = sys.argv[1]
filename = sys.argv[2]

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connent((host,port))

s.sendall(filename + "\r\n")

while 1:
    buf = s.recv(all)
    if not len(buf):
        break
    sys.stdout.write(buf)
	

#!/usr/bin/python
#Filename: socket_client1.py

import socket,sys
host = sys.argv[1]
port = 10087

f = file(r'readfile.txt','r')
fileread = f.read()

s =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
s.sendall(fileread)
data=s.recv(1024)
s.close()
print 'Received:',repr(data)

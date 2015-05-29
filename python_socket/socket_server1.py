#!/usr/bin/python
#Filename: socket_server1.py

import socket,sys
HOST = ''
PORT = 10087
data = ''
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
conn,addr = s.accept()
print 'Connected by' , addr
while 1:
    data = conn.recv(1024)
    if not data:break
    print '-'*10
    print data
    print '-'*10
    conn.sendall(data)
    f = file(r'testsave.txt','a+')
    f.write(data)
    f.close()
conn.close()    
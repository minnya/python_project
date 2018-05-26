from socket import *

HOST = 'localhost'
PORT = 50007

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
while 1:
    msg = input()
    if msg == '.':
        break;

    s.send(msg.encode("utf-8"))

    data = s.recv(1024)
    if not data:
        print( 'End')
        break

    print( 'Returned message :', data)

s.close()

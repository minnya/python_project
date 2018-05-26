from socket import *

HOST = 'localhost'
PORT = 50007

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
(conn, addr) = s.accept()

print('Connected by',addr)

while 1:
    data = conn.recv(1024)
    if not data:
        print( 'End')
        break

    print ("Data receive : ",data)

    msg = input()
    if msg == ".":
        break
    conn.send(msg.encode("utf-8") )

conn.close()

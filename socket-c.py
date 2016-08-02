from socket import *
import time

HOST='127.0.0.1'
PORT=8888
BUFFSIZE=1024
ADDR=(HOST,PORT)

sock=socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)
data=[1,2,3,4,5,6,7]
for i in data:
    print(i)
    time.sleep(1)
    sock.send(str(i))

time.sleep(10)
sock.send("q")
sock.close()

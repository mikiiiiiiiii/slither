from socket import *

HOST='127.0.0.1'
PORT=8888
BUFFSIZE=1024
ADDR=(HOST,PORT)

sock=socket(AF_INET, SOCK_STREAM)
sock.bind(ADDR)
sock.listen(5)

STOP_CHAT=False

while not STOP_CHAT:
    print("waiting for address"+ HOST + ":" +str(PORT))
    tcpClientSocket, addr=sock.accept()
    print("connected", addr)
    while True:
        try:
            data=tcpClientSocket.recv(BUFFSIZE)
        except:
            tcpClientSocket.close()
            break
        if not data:
            print("not data")
            break
        print(data)
#        tcpClientSocket.send(" ")
        if data.upper()=="Q" or data.upper()=="QUIT":
            STOP_CHAT=True
        if STOP_CHAT:
            break

tcpClientSocket.close()
sock.close

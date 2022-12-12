import socket
import threading
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5600
FORMAT = 'ascii'
ADDR = (HOST, PORT)
SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(10)

def ReceiveMess(role):
    return role.recv(SIZE).decode(FORMAT)
def SendMess(role, msg):
    role.send(msg.encode(FORMAT))

client = [['none' for j in range(4)] for i in range(2)]
room = [['none' for j in range(4)] for i in range(2)]
numbPlayers = [[i,2] for i in range(2)]

def Handle_client(sv, addr):
    connect = True

    # while connect:
    #     command = ReceiveMess(sv)
    #     if (command=='close'): connect = False
    #     elif (command!='none'):
    #         print(command)
    #     SendMess(sv, 'done')
    sv.close()


while True:
    sv, addr = server.accept()
    ThreadTreat = threading.Thread(target=Handle_client, args=(sv, addr,))
    ThreadTreat.start()
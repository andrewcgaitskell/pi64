## https://stackoverflow.com/questions/65057745/how-do-i-handle-a-disconnect-with-python-sockets-connectionreseterror

import socket
import threading


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Connection oriented, IPV4

s.bind((socket.gethostname(), 5010))#Ip address information, port
s.listen(5)

connections = [] #Connection added to this list every time a client connects

def accptconnection():
    while True:
        clientsocket, address = s.accept()
        connections.append(clientsocket) #adds the clients information to the connections array
        threading.Thread(target=recvmsg, args=(clientsocket, address,)).start()

def recvmsg(clientsocket, address):
    print(f"Connection from {address} has been established.")
    while True:
        try:
            msg = clientsocket.recv(9)
        except ConnectionError:
            print(f"Connection from {address} has been lost.")
            if clientsocket in connections:
                connections.remove(clientsocket)
            return
        if len(msg.decode('utf-8')) > 0:
            print(msg.decode("utf-8"))
        for connection in connections: #iterates through the connections array and sends message to each one
            msgbreak = msg
            try:
                connection.send(bytes(str(msgbreak.decode("utf-8")), "utf-8"))
            except ConnectionError:
                 print(f"Unable to reach client with socket {connection}")
                 if connection in connections:
                     connections.remove(connection)

accptconnection()

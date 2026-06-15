import socket
import threading

PORT = 5656
HOST = socket.gethostbyname(socket.gethostname())
fmt = 'ascii'
buff = 512

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("listening...")
clients = []
nicknames = []

def broadcast(msg):
    for i in clients:
        try:
            i.send(msg)
        except:
            pass

def handle_client(client):
    while True:
        try: #recieve and broadcast
            msg = client.recv(buff)
            broadcast(msg)
        except: #disconnects
            ind = clients.index(client)
            clients.remove(client)
            client.close()
            nn = nicknames[ind]
            broadcast(f"{nn} left!".encode(fmt))
            nicknames.remove(nn)
            break

def receive():
    print("Server running....")
    while True:
        client, adr = server.accept()
        print(f"connected with {str(adr)}")
        client.send("nick".encode(fmt))
        nn = client.recv(buff).decode(fmt)
        clients.append(client)
        nicknames.append(nn)
        broadcast(f"{nn} joined the chat!".encode(fmt))
        client.send("Connected to server!".encode(fmt))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
receive()
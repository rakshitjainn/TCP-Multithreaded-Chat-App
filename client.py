import socket
import threading

PORT = 5656
HOST = socket.gethostbyname(socket.gethostname())
fmt = 'ascii'
buff = 512

nn = input("Choose nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            msg = client.recv(buff).decode(fmt)
            if msg == 'nick':
                client.send(nn.encode(fmt))
            else:
                print(msg)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        msg = f'{nn}: {input("")}'
        client.send(msg.encode(fmt))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
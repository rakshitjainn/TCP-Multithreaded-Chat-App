import socket
import threading
import psycopg2
from psycopg2 import pool

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
            decoded = msg.decode(fmt)
            if ":" in decoded:
                sender, text = decoded.split(":", 1)
                db.save_message(sender.strip(), text.strip())
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
        history = db.get_chat_history()
        if history:
            client.send("\nChat History: \n".encode(fmt))
            for sender, text in history:
                client.send(f"{sender}: {text}\n".encode(fmt))
            client.send("--------------------\n".encode(fmt))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
class ChatDatabase:
    def __init__(self):
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            1, 10, 
            user="postgres", 
            password="admin123", 
            host="127.0.0.1", 
            port="5432", 
            database="chat_app"
        )

    def save_message(self, sender, body):
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO messages (sender, message_body) VALUES (%s, %s);", (sender, body))
                conn.commit()
        except:
            conn.rollback()
        finally:
            self.pool.putconn(conn)
    def get_chat_history(self, limit=20):
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT sender, message_body FROM messages ORDER BY timestamp DESC LIMIT %s;", (limit,))
                return cursor.fetchall()[::-1]
        except:
            return []
        finally:
            self.pool.putconn(conn)
db = ChatDatabase()
receive()
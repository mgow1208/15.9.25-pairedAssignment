# WE COULD NOT GET IT TO WORK SINCE IT SAYS WE NEED TO CHANGE FIREWALL SETTINGS, NEITHER OF US HAVE ADMIN PERMISIIONS

import socket
import threading

# Set the server host to your local IP address
host = '62.255.239.150'  # Replace this with your local IP
port = 80  # The port for the connection

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# Broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle communication with each client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)  # Broadcast the message to all clients
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Accept new client connections
def receive():
    print(f"Server is listening on {host}:{port}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Start receiving connections
receive()


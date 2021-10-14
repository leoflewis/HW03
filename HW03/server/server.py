#Server

from socket import *
from threading import *
import sys

server = socket(AF_INET, SOCK_STREAM)

serverPort = 56003
server.bind(('',serverPort))
server.listen(100)

list_of_clients = []

def clientThread(conn, addr):
	name = conn.recv(1024).decode()
	conn.send(("Welcome to this chatroom " + name + "!").encode())
	while True:
		try:
			message = conn.recv(2048).decode()
			
			if message == "EX":
				EX(conn)
				return
			
			elif message:
				print(name + ": " + message)
				response = "Recieved " + message
				broadcast(response, conn)
		except:
			remove(conn)
			server.close()
				
def EX(conn):
	remove(conn)

def broadcast(message, connection):
	for client in list_of_clients:
		if client != connection:
			client.send(message.encode())

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)
		connection.close()
		
		
while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print(addr[0] + " connected")
	thread = Thread(target = clientThread,args = (conn,addr))
	thread.start()

server.close()
sys.exit()
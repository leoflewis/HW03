#Server
#get test

from socket import *
from threading import *
import sys

server = socket(AF_INET, SOCK_STREAM)

serverPort = 56003
server.bind(('',serverPort))
server.listen(100)

clients = {}

def clientThread(conn, addr, name):
	
	conn.send(("Welcome to this chatroom " + name + "!").encode())
	while True:
		try:
			message = conn.recv(2048).decode()
			
			if message == "EX":
				EX(conn)
				return
				
			if message == "PM":
				PM(conn)
				
			if message == "DM":
				DM(conn)

		except:
			remove(conn)
			server.close()
				
def EX(conn):
	remove(conn)
	
def PM(conn):
	conn.send(("Please Enter Public Message: ").encode())
	message = conn.recv(2048).decode()
	broadcast(message, conn)
	
def DM(message):
	conn.send(("Please Enter Direct Message: ").encode())

def broadcast(message, connection):

	for x in clients:
		if connection != x:
			message = "Incoming PM: " + message + "\n"
			x.send(message.encode())
		else:
			x.send(("Public Message: '" + message + "' Sent to all users\n").encode())

def remove(connection):
	print(clients[connection] + " disconnected")
	connection.close()
	del clients[connection]
	
		
while True:
	conn, addr = server.accept()
	name = conn.recv(1024).decode()
	
	clients[conn] = name
	
	print(name + " connected")
	thread = Thread(target = clientThread,args = (conn,addr,name))
	thread.start()

server.close()
sys.exit()

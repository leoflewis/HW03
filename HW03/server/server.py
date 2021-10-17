#Server
#get test new branch

from socket import *
from threading import *
import sys

server = socket(AF_INET, SOCK_STREAM)

serverPort = 56004
server.bind(('',serverPort))
server.listen(100)

clients = {}

def clientThread(conn, addr, name):
	
	conn.send(("DWelcome to this chatroom " + name + "!").encode())
	while True:
		try:
			message = conn.recv(2048).decode()
			
			if message == "EX":
				EX(conn)
				return
				
			if message == "PM":
				PM(conn)
				
			if message == "DM":
				PM(conn)

		except:
			remove(conn)
			server.close()
				
def EX(conn):
	remove(conn)
	
def PM(conn):
	conn.send(("CPPlease Enter Public Message: ").encode())
	message = conn.recv(2048).decode()
	broadcast(message, conn)
	
def DM(conn):
	listUsers = list(clients.values())
	conn.send(("CPList of online users: ").encode())
	for x in listUsers:
		if (myDict.get(conn)) != x:
			conn.send((user + ", ").encode())
		conn.send("CPPlease select a user: ")
			
	conn.send()

def broadcast(message, connection):
	messageSend = "CB\nIncoming PM: " + message + "\n"
	for x in clients:
		if connection != x:
			x.send(messageSend.encode())
		else:
			x.send(("CPPublic Message: '" + message + "' Sent to all users\n").encode())

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

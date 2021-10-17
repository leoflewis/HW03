#Server
#get test new branch

from socket import *
from threading import *
import sys

server = socket(AF_INET, SOCK_STREAM)

serverPort = 56002
server.bind(('',serverPort))
server.listen(100)

clients = {}

def clientThread(conn, addr, name):
	
	conn.send(("DWelcome to this chatroom " + name + "!").encode())
	while True:
		#try:
		message = conn.recv(2048).decode()

		if message == "EX":
			EX(conn)
			return

		if message == "PM":
			PM(conn)

		if message == "DM":
			DM(conn)

		#except:
		#	remove(conn)
		#	server.close()
				
def EX(conn):
	remove(conn)
	
def PM(conn):
	conn.send(("CPPlease Enter Public Message: ").encode())
	message = conn.recv(2048).decode()
	broadcast(message, conn)
	
def DM(conn):
	listUsers = list(clients.values())
	message = "CDList of online users:\n"
	print(message)
	
	#create string of avaliable users
	for x in listUsers:
		if (clients.get(conn)) != x:
			message = message + x + "\n"
		else:
			sendUser = x
			
	print(message)
	conn.send(message.encode())
	returnString = conn.recv(2048).decode()
	print(returnString)
	
	recvUser, recvMessage = returnString.split('|')
	
	if(recvUser in listUsers):
		print("Valid User")
		for key, value in clients.items():
			if recvUser == value:
				connDM = key
		
		conn.send(("CBMessage sent to " + recvUser +"\n").encode())
		connDM.send(("CB\nDM from " + sendUser + ": " + recvMessage + "\n").encode())
	else:
		print("Invalid User")


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

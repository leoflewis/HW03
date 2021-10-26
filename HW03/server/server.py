#Server
#get test new branch

from socket import *
from threading import *
import sys

server = socket(AF_INET, SOCK_STREAM)

serverPort = int(sys.argv[1])
server.bind(('',serverPort))
server.listen(100)

clients = {}

#passwords are stored 'username;password'
password_file = "passwords.txt"

#writes new user passwords to file
def save_passwords(password, name):
	f = open("passwords.txt", "a")
	f.write(name + ";" + password + "\n")
	f.close()

#returns passwords and names from file
def get_passwords():
	try:
		f = open("passwords.txt", "r")
		lines = f.readlines()
		passwords = []
		names = []
		for line in lines:
			phrase = line.split(";")
			passwords.append(phrase)
			names.append(phrase[0])
		f.close()
	except FileNotFoundError:
		#if password file is removed or deleted, this will build one from scratch with an admin account
		f = open("passwords.txt", "w")
		f.write("admin;admin\n")
		f.close()
		passwords = []
		names = []
	return passwords, names

def login(password, name, conn):
	passwords, names = get_passwords()
	if name not in names:
		#L character denotes login related commands
		conn.send(("L(New user your password saved)\n\nWelcome To The Chatroom!\n").encode())
		save_passwords(password, name)
		return True
	for word in passwords:
		if word[0] == name:
			if password == word[1].replace('\n', ''):
				print("success")
				conn.send(("L(Successfully logged on.)\n\nWelcome To The Chatroom!\n").encode())
				return True
			else:
				print("login failed")
				conn.send(("FIncorrect password - login failed\n").encode())
				#client will close when it receives LF
				return False


def clientThread(conn, addr, name):
	
	#conn.send(("DWelcome to this chatroom " + name + "!\n").encode())
	while True:
		#try:
		message = conn.recv(2048).decode()

		#client sends password in format 'password;<actual password>'
		if message[0:9] == "password;":
			result = login(message[9:],name, conn)
			#conn.send(("DWelcome to this chatroom " + name + "!\n").encode())
			if result == False:
				EX(conn)
				return
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
	conn.send(("D\nPlease Enter Public Message: ").encode())
	message = conn.recv(2048).decode()
	broadcast(message, conn)
	
def DM(conn):
	listUsers = list(clients.values())
	message = "D~~~~~~~~~~~~~~~~~~~~~~~\nList of online users:\n"
	#print(message)
	
	#create string of avaliable users
	for x in listUsers:
		if (clients.get(conn)) != x:
			message = message + x + "\n"
		else:
			sendUser = x
			
	#print(message)
	message = message + "~~~~~~~~~~~~~~~~~~~~~~~\n"
	conn.send(message.encode())
	returnString = conn.recv(2048).decode()
	#print(returnString)
	
	recvUser, recvMessage = returnString.split('|')
	
	if(recvUser in listUsers):
		print("Valid User")
		for key, value in clients.items():
			if recvUser == value:
				connDM = key
		
		conn.send(("CBMessage sent to " + recvUser +"\n-------------------------").encode())
		connDM.send(("CB\n-------------------------\nDM from " + sendUser + ": " + recvMessage + "\n-------------------------").encode())
	else:
		print("Invalid User")


def broadcast(message, connection):
	messageSend = "CB\n-------------------------\nIncoming PM: " + message + "\n-------------------------"
	for x in clients:
		if connection != x:
			x.send(messageSend.encode())
		else:
			x.send(("CP\nPublic Message: '" + message + "' Sent to all users\n-------------------------").encode())

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

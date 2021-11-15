#Server program, Creates a new thread per connected client. Uses specified port number to create socket.
#When client connectes, the server will see if the username is existing or new.
#If existing, the server will request the password for the user, and either accept the conenction or deny it.
#If new, the server will request a password, and save it to the file of users / passwords.
#Each active client is added to a dictionary conatining the name / socket info.
#When a command is called, the server will recieve / reply to the client for extra data, or to send a message from another user.
#Colin Bolduc -- DD7266BL


from socket import *
from threading import *
import sys

#attempt to create new socket for server.
try:
	server = socket(AF_INET, SOCK_STREAM)
except socket.error as e:
	print("Error creating socket: " + e)
	sys.exit()

#get port from command line when program called. Must be int.
try:
	serverPort = int(sys.argv[1])
except ValueError as e:
	print("Server Port must be an int value.")
	sys.exit()

#Bind port to server socket.
server.bind(('',serverPort))
server.listen(100)

#New dictionary of active clients.
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

#Handles login procedure
def login(password, name, conn):
	#use get_passwords() function to load user / pass.
	passwords, names = get_passwords()
	#New user, create password.
	if name not in names:
		#L character denotes login related commands
		conn.send(("L(New user your password saved)\n\nWelcome To The Chatroom!\n").encode())
		save_passwords(password, name)
		return True
	#Existing user, request password.
	for word in passwords:
		if word[0] == name:
		#If correct, login success
			if password == word[1].replace('\n', ''):
				#print("success")
				conn.send(("L(Successfully logged on.)\n\nWelcome To The Chatroom!\n").encode())
				return True
			#If incorrect, login fail.
			else:
				#print("login failed")
				conn.send(("FIncorrect password - login failed\n").encode())
				#client will close when it receives LF
				return False

#Main client function, will await new commands from the client.
def clientThread(conn, addr, name):
	try:
		while True:
			#Recieves command from client, either will be used for login, PM, DM or EX.
			message = conn.recv(2048).decode()

			#client sends password in format 'password;<actual password>'
			if message[0:9] == "password;":
				result = login(message[9:],name, conn)
				if result == False:
					conn.close()
					del clients[conn]
					return
			if message == "EX":
				EX(conn)
				return

			if message == "PM":
				PM(conn)

			if message == "DM":
				DM(conn)
	except:
		conn.close()
		sys.exit()

#Removes active client from active client lists.	
def EX(conn):
	conn.send(("CX").encode())#Send a closing message to the client in order to close the listener thread.
	#print("DEBUG: user left.")
	conn.close()
	del clients[conn]

#Sends a Public Message to every other active user, promts requesting user for message.
def PM(conn):
	conn.send(("CPack").encode())
	message = conn.recv(2048).decode()
	messageSend = "D\nIncoming PM: " + message + "\n"
	for x in clients:
		if conn != x:
			x.send(messageSend.encode())
		else:
			x.send(("CSack").encode())

#Will send a message to one specified user. Will send a list of active users to requester, and send the message to them.
def DM(conn):
	listUsers = list(clients.values())
	message = "CI\nList of online users:\n"
	
	#create string of avaliable users
	for x in listUsers:
		if (clients.get(conn)) != x:
			message = message + x + "\n"
		else:
			sendUser = x
			
	#Send the list of online users to the client, wait for ACK.
	conn.send(message.encode())
	returnAck = conn.recv(1024).decode()
	if returnAck != "ack":
		return
	#Send an ACK to the client to signal the next step.
	conn.send(("CDack").encode())
	returnString = conn.recv(2048).decode()
	recvUser, recvMessage = returnString.split('|')
	
	#Check the user requested by the client. If valid, continue, else send fail
	if(recvUser in listUsers):
		#Get the connection data if the user is valid
		for key, value in clients.items():
			if recvUser == value:
				connDM = key
		conn.send(("CMack").encode())
		returnAck2 = conn.recv(1024).decode()
		if returnAck2 != "ack":
			return
		connDM.send(("D\nDM from " + sendUser + ": " + recvMessage + "\n").encode())
	elif(recvUser not in listUsers):
		conn.send(("CZack").encode())
		#returnAck3 = conn.recv(1024).decode()
		

	
		
while True:
	#Accept new client conenction
	conn, addr = server.accept()
	name = conn.recv(1024).decode()
	
	#Create a new entry using connection & username data.
	clients[conn] = name
	
	#print(name + " connected")
	thread = Thread(target = clientThread,args = (conn,addr,name))
	thread.start()

server.close()
sys.exit()

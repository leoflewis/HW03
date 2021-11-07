#Client program, will use given hostname, prot number and user name to open a connection to the server program.
#The client will then initiate the log-in procedure, before generating the new thread.
#Once log-in is successful, the program will split into two threads, the existing one will listed for incoming messages from the server.
#The second / new thread will await for user input, and run the specified commands.
#When PM is called, the server will recieve the command, and prompt the user for the message to send to other users, and will confirm the status.
#When DM is called, the server will give a list of other active users, requesting which one will the the target, plus the message. Will confirm status.
#When EX is called, the client will send EX to the server, and disconnect. The server will remove the client from the active list.
#Colin Bolduc -- DD7266bl
#

from socket import *
from threading import *
import time
import sys, os

#Create socket connection
try :
	connection = socket(AF_INET, SOCK_STREAM)
except socket.error as e:
	print ("Error creating socket: " + e)
	sys.exit()

#Get server connection data from terminal input
try:
	hostname = str(sys.argv[1])
	port = int(sys.argv[2])
	name = str(sys.argv[3])
except ValueError as e:
	print("Server Port must be an integer value.")
	sys.exit()


#Connect to the server, send given username to server.
try:	
	connection.connect((hostname, port))
except socket.gaierror as e:
	print("Address related error conencting to server: " + e)
	sys.exit()
except socket.error as e:
	print("Connection Error: " + e)
	sys.exit()
	
connection.send(name.encode())

#Handles sending data for PM messages.
def PM():
	connection.send(("PM").encode()) 
	time.sleep(1)
	x = input()
	connection.send(x.encode())

#Handles sending data DM messages.
def DM():
	connection.send(("DM").encode())
	time.sleep(1) #wait for 1 second for server to send list of clients.
	user = input("Select a user: ")
	message = input("Mesage to send: ")
	serverMessage = user + "|" + message 
	connection.send(serverMessage.encode())	#Send selected user + message to server.

#Handles closing the client connection + notify server.
def EX():
	print("Closing connection.")
	connection.send(("EX").encode())
	connection.close() 
	sys.exit()

#Handles login data, closes conneciton if password is deemed false by server (return user).
def login(password):
	connection.send(("password;"+password).encode())
	message = connection.recv(1024).decode()
	
	#If rresponse is L, login was successful, begin wait for command phase.
	if(message[0] == 'L'):
		print(message[1:])
		print("Please Enter a command: ")

	#If response is F, login was unsuccessful (return user), exit program.
	if message[0] == 'F':
		print(message[1:])
		connection.close()
		sys.exit()

def userInput():
	#Accepts one of three commands when user is in ready for command state.
	while True:
		x = input()
		if x == "PM" or x == "Pm" or x == "pM" or x == "pm":
			PM()
		elif x == "DM" or x == "Dm" or x == "dM" or x == "dm":
			DM()
		elif x == "EX" or x == "Ex" or x == "eX" or x == "ex":
			EX()
		else:
			print("Invalid Command!")
			continue

#Prompts login functionality.
password = input("Enter password for " + name + ": ")
login(password)

#Starts the thread that will recieve commands from the user to send to server.
thread = Thread(target = userInput, name = 'command')
thread.start()


#This loop waits for responses from server, promps user for new command when function is finished.
while True:
	try:
		message = connection.recv(2048).decode()
	
		if(message[0] == 'D'):
			print(message[1:])
		if(message[0] == 'C'):
			command = message[1]
			print(message[2:])
			if(command == 'B'):
				print("Please Enter a command: ")
	except:
		connection.close()
		sys.exit()
			
connection.close()
sys.exit()

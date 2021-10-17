#Client
from socket import *
from threading import *
import time
import sys

connection = socket(AF_INET, SOCK_STREAM)

hostname = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])
connection.connect((hostname, port))
connection.send(name.encode())

def PM():
	print("\n")
	connection.send(("PM").encode())
	x = input()
	connection.send(x.encode())

def DMR():
	print("\n")
	connection.send(("DM").encode())
	time.sleep(1)
	user = input("Select a user: ")
	message = input("Mesage to send: ")
	serverMessage = user + "|" + message 
	connection.send(serverMessage.encode())	#Send selected user + message to server.


def EX():
	print("Closing connection.")
	connection.send(("EX").encode())
	connection.close()
	sys.exit()

def userInput():
	time.sleep(.5)
	print("Please Enter a command: ")
	while True:
		x = input()
		if x == "PM" or x == "Pm" or x == "pM" or x == "pm":
			PM()
		elif x == "DM" or x == "Dm" or x == "dM" or x == "dm":
			DMR()
		elif x == "EX" or x == "Ex" or x == "eX" or x == "ex":
			EX()
		else:
			print("Invalid Command!")
			continue



thread = Thread(target = userInput, name = 'command')
thread.start()


	
while True:
	try:
		message = connection.recv(1024).decode()
		if(message[0] == 'D'):
			#print("Caught Data Command")
			print(message[1:])
		if(message[0] == 'C'):
			command = message[1]

			print(message[2:])
			if(command == 'B' or command == 'P'):
				print("Please Enter a command: ")
			if(command == 'D'):
				message = connection.recv(1024).decode()
				print(message)
				#response = connection.recv(1024).decode()
				print("Please Enter a command: ")
	except:
		connection.close()
		sys.exit()
			
connection.close()
sys.exit()
#Client
from socket import *
from threading import *
import sys

connection = socket(AF_INET, SOCK_STREAM)

hostname = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])
connection.connect((hostname, port))
connection.send(name.encode())

def PM():
	connection.send(("PM").encode())

def DM():
	connection.send(("DM").encode())

def EX():
	print("Closing connection.")
	connection.send(("EX").encode())
	
	connection.close()
	sys.exit()

def userInput():
	while True:

		print("Please enter a command!")
		x = input()
		if x == "PM":
			PM()
		elif x == "DM":
			DM()
		elif x == "EX":
			EX()
		else:
			print("Invalid Command!")
			continue



thread = Thread(target = userInput)
thread.start()


	
while True:
	try:
		message = connection.recv(1024).decode()
		print(message)
	except:
		connection.close()
		sys.exit()
			
connection.close()
sys.exit()
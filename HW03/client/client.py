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
	time.sleep(.5)

def DM():
	print("\n")
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
		if x == "PM" or x == "Pm" or x == "pM" or x == "pm":
			PM()
		elif x == "DM" or x == "Dm" or x == "dM" or x == "dm":
			DM()
		elif x == "EX" or x == "Ex" or x == "eX" or x == "ex":
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
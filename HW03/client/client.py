#Client program, will use given hostname, prot number and user name to open a connection to the server program.
#The client will then initiate the log-in procedure, before generating the new thread.
#Once log-in is successful, the program will split into two threads, the existing one will listed for incoming messages from the server.
#The second / new thread will await for user input, and run the specified commands.
#When PM is called, the server will recieve the command, and prompt the user for the message to send to other users, and will confirm the status.
#When DM is called, the server will give a list of other active users, requesting which one will the the target, plus the message. Will confirm status.
#When EX is called, the client will send EX to the server, and disconnect. The server will remove the client from the active list.
#When recieving a message, the listener thread will add commands to the queue, or queue messages if the user is busy.
#Colin Bolduc -- DD7266bl
#Leonardo Lewis -- XW3440RF
#
try:

	from socket import *
	from threading import *
	import time
	import sys, os

	queue = [] #Queue of server responses / messages.
	busy = False #prevents messages from being printed to UI when user is in a function.

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

	connection.connect((hostname, port))


	connection.send(name.encode())

	#Handles login data, closes conneciton if password is deemed false by server (return user).
	def login(password):
		connection.send(("password;"+password).encode())
		message = connection.recv(1024).decode()

		#If rresponse is L, login was successful, begin wait for command phase.
		if(message[0] == 'L'):
			print(message[1:])
			#print("Please Enter a command: ")

		#If response is F, login was unsuccessful (return user), exit program.
		if message[0] == 'F':
			print(message[1:])
			connection.close()
			sys.exit()

	#Drives the DM functionality, sending / waiting for ACK from server.
	def PM():
		connection.send(("PM").encode()) 
		while not ("Pack" in queue):
			time.sleep(.1)
		if "Pack" in queue: #
			queue.remove("Pack")
			print("Please Enter Message: ")
			message = input()
			connection.send((message).encode()) 
			while not ("Sack" in queue):
				time.sleep(.1)
			if "Sack" in queue:
				queue.remove("Sack")
				print("\nPublic Message: '" + message + "' Sent to all users\n")
				print("Please Enter A Command: ")

	#Drives the DM functionality, sending / waiting for ACK from server.
	def DM():
		connection.send(("DM").encode())
		while not ("Dack" in queue):
			time.sleep(.1)
		if "Dack" in queue:
			queue.remove("Dack")
			user = input("Select a user: ")
			message = input("Mesage to send: ")
			serverMessage = user + "|" + message 
			connection.send(serverMessage.encode())	#Send selected user + message to server.
			#queue.append("Mack")
			while not (("Mack" in queue) or ("Zack" in queue)):
				time.sleep(.1)
			if "Mack" in queue:
				queue.remove("Mack")
				print("DM sent to " + user +"\n")
			if "Zack" in queue:
				queue.remove("Zack")
				print("DM failed: Invalid User!\n")
			print("Please Enter A Command: ")

	#Drives the closing of the client. Sends closing command, then waits for listener function to end before shutting down.
	def EX():
		print("Closing connection.")
		connection.send(("EX").encode())
		thread.join()
		connection.close() 
		sys.exit()
			

	def userInput():
		#Accepts one of three commands when user is in ready for command state.
		while True:
			global busy
			busy = False
			if len(queue) != 0:
				print("Message Backlog:")
				for mes in queue:
					print(mes[1:])
					queue.remove(mes)
				print("Please Enter A Command: ")
			x = input()
			if x == "PM" or x == "Pm" or x == "pM" or x == "pm":
				busy = True
				PM()
			elif x == "DM" or x == "Dm" or x == "dM" or x == "dm":
				busy = True
				DM()
			elif x == "EX" or x == "Ex" or x == "eX" or x == "ex":
				busy = True
				EX()
			else:
				print("Invalid Command!")
				print("Please Enter A Command: ")
				continue

	def listener():
			#This loop waits for responses from server, promps user for new command when function is finished.
			while True:
				try:
					message = connection.recv(2048).decode()
					#print("DEBUG : recieved: " + message[1:])
					
					#If message is empty, we will not do anything, and instead wait for next message.
					if (len(message) >= 1):

						#Catches data messages, if client is currently running a PM, DM or EX command, it will be queued and printed later.
						if(message[0] == 'D'):
							if busy == False:
								print(message[1:])
								print("Please Enter A Command: ")
							else:
								queue.append(message)
								
						#Catches command messages.
						if(message[0] == 'C'):
							#If comamnd is I, we will print the list of online users for DM.
							if(message[1] == 'I'):
								print(message[2:])
								connection.send(("ack").encode()) #Tells server we are ready for next request.
							#I
							elif(message[1] == 'M'):
								queue.append(message[1:])
								connection.send(("ack").encode())
							elif(message[1] == 'X'): #Server sends close message to the listener, which shuts down the thread.
								return
							elif(message[1] == 'Z'): #failed ack
								queue.append(message[1:])
								connection.send(("ack").encode())
							else:
								queue.append(message[1:])

					else:
						continue

				except:
					connection.close()
					sys.exit()


	#Prompts login functionality.
	password = input("Enter password for " + name + ": ")
	login(password)

	#Starts the thread that will recieve commands from the user to send to server.
	thread = Thread(target = listener)
	thread.start()
	print("Please Enter A Command: ")
	userInput()
	
	#Close the connection / program if functions nto running.
	connection.close()
	sys.exit()
except KeyboardInterrupt: #Closes the program safely for the server if crtl+c is called.
	connection.close()
	sys.exit()
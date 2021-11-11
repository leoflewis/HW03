Assignment 3 Readme

This project contains a program to run a server and a program to run a client that connects to the server. 

To run the server program:
  navigate to the server directory within HW03 and run the command:
  python3 server.py <port-number>
  where the <port-number> is replaced with your desired port number.
 
To run the client program:
  navigate to the client directory within HW03 and run the command:
  python3 client.py <host-name> <port-number> <user-name>
  where the <host-name> is replaced with the host of the server program
  and the <port-number> is replaced with the port number the server is bound to 
  and <user-name> is replaced with your desired user name.
  
Once the server is running and a client attempts to connect, the first thing they will be prompted for is a password.
Within the server directory there should be a file named 'passwords.txt' that stores the user name and passwords in the format 
'user-name;password'. If the file does not exist, the server will build one from scratch and add 'admin;admin' as a default account.
If a user is loging on for the first time, the server will store their password and notify the user of this.
If the server has been running previously, it will check within the 'passwords.txt' file to see if there is an entry for the user.
If user's name is stored with a corresponding password, the server will expect that password. 
If the password is incorrect the user will not connect and will have to run client.py another time to try again. 

Once a client has logged in they will be prompted for a command, there are a few commands they can enter.
1) PM. The client can send a public message to everyone connected to the server. To do this, the client enters pm, the server will 
respond by prompting for the message to send.
2) DM. The client can send a direct message to anyone connected to the server. To do this, the client enters dm, the server responds with a
list of all connected users, the client replies with their desired user, the server reqeusts the message to be sent and the client replies 
with their message.
3) EX. The client can close their connecttion by entering EX when prompted for a command. 

In addition to this functionality on the client side the server side will dislay some messages while it is running.
The server will print the result of login attempts, whether they fail or succeed.
The server will print the result of attempts to direct message other users. It will also print the message and the user.
Finally, the server will print some of the acknowledgements it sends to the client.  

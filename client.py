#!/usr/bin/python3

import socket
import subprocess

import sys
if(len(sys.argv) > 2):
    REMOTE_HOST=sys.argv[1]
    REMOTE_PORT=int(sys.argv[2])

    client = socket.socket()
    print("[-] Connection Initiating...")
    client.connect((REMOTE_HOST, REMOTE_PORT))
    print("[-] Connection initiated!")

    command=""
    while command!="exit":
        command = input('Enter Command : ')
        
        commandencode = command.encode()
        client.send(commandencode)
        print('[+] Command sent')
        output = client.recv(1024)
        output = output.decode()
        print(f"Output: {output}")

    client.close()
    print("Cerrando conexión")  
else:
    print ("Necesario ejecutar con al menos dos parámetros")
    print ("./client.py param1 param2")


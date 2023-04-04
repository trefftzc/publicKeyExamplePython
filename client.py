import socket

import rsa

host = 'localhost'
port = 2080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # connect to server
    client_socket.connect((host, port))
    
    # get user input
    # num = input('Enter a number: ')
    initial_message = 'Send Pub Key'
    # send number to server
    client_socket.send(initial_message.encode())
    
    # receive and print response from server
    response = client_socket.recv(1024)
    serverKeyPub = rsa.key.PublicKey.load_pkcs1(response, format='DER')
    # response = response.replace("\r\n",'')
    # serverKeyPub  = rsa.importKey(response)
    message = 'Hello!'.encode('utf8')
    # message = 'Hello!'
    encrypted = rsa.encrypt(message,serverKeyPub)
    client_socket.send(encrypted)
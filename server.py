#!/usr/bin/env python3
#
# A server that sends his private key to a client.
# The client sends its public key to the client.
# The client encodes its message with the public key
# and sends it back to the server.
# The server uses its private key to decrypt
# the message sent by the client
# Base on the example available at
# https://stuvel.eu/python-rsa-doc/usage.html#generating-keys
#
import argparse

import sys
import itertools
import socket
from socket import socket as Socket

import rsa

def main():
	(server_pub,server_priv) = rsa.newkeys(512)
	# Command line arguments. Use a port > 1024 by default so that we can run
	# without sudo, for use as a real server you need to use port 80.
	parser = argparse.ArgumentParser()
	parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
	args = parser.parse_args()
	with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(('', args.port))
		server_socket.listen(1)
		print("server ready")
		while True:
			connection_socket, client_address = server_socket.accept()
			try:
				request = connection_socket.recv(1024).decode('ascii')
				print("\n\nReceived request")
				print("======================")
				print(request.rstrip())
				server_pub_as_string = server_pub.save_pkcs1(format='DER')
				connection_socket.send(server_pub_as_string)
				print("Send public key ",server_pub_as_string)
				encryptedMessage = connection_socket.recv(1024)
				message = rsa.decrypt(encryptedMessage, server_priv)
				# message = 
				#print("======================")
				#print("\n\nThen received encrypted msg, which was")
				print("======================")
				print(message.rstrip())
				print("======================")
			except ValueError:
				print("error reading value from client")
		return 0


if __name__ == "__main__":
    sys.exit(main())
import socket

global HOST 
HOST = "10.1.1.11"
global PORT
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

greatings = "Hello"
s.send(greatings.encode())

server_response = s.recv(1024)

print(server_response.decode())
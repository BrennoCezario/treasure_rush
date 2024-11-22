import socket

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 5000     

# Criação do socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Recebe mensagem do servidor
mensagem = client_socket.recv(1024)
print(f"Mensagem do servidor: {mensagem.decode('utf-8')}")

client_socket.close()
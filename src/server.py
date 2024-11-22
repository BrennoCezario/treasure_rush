import socket

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 5000 

# Criação do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5) 

print(f"Servidor iniciado. Aguardando conexões em {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"Conexão estabelecida com: {addr}")
conn.sendall(b"Bem-vindo ao servidor!")


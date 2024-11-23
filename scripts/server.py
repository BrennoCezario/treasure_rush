import socket
import threading

# Server Init Function -->
def start_server():
    host = '127.0.0.1'
    port = 5000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"Servidor iniciado. Aguardando conexões em {host}:{port}...")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Conexão estabelecida com: {addr}")
        conn.sendall(b"Bem-vindo ao servidor!")
        
# <-- 

if __name__ == "__main__":
    start_server()
    
    main_map_size = 5
    main_map = [[0 for i in range(main_map_size)] for i in range(main_map_size)]
    
    for i in main_map:
        print(i)
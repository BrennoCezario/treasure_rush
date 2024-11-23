import socket

# Server Init Function -->
def start_client(player):
    host = '127.0.0.1'
    port = 5000
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    mensagem = client_socket.recv(1024)
    print(f"Mensagem do servidor: {mensagem.decode('utf-8')} -> Jogador: {player.name}")

    client_socket.close()
# <--

class Player:
    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    player_name = input("Digite um nome para seu personagem: ")
    player = Player(player_name)   
    start_client(player)
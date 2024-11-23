# Configurações iniciais

# Criar Loop Infinito 

# Desenhar os objetos do jogo na tela
# personagem do jogador 
# pontuação
# tesouro

# Desenhar Mapa do jogo na tela
# mapa principal
# mapa do tesouro

# Criar Lógica de iniciar a partida
# Requisitos:
# sala existente
# sala com host 
# sala com no mínimo 2 jogadores e no máximo 4
# jogadores não hosts precisam permitir o início
# Para iniciar:
# Host inicia partida
        
# Criar Lógica de terminar a partida
# todos os tesouros são coletados
# resta um único jogador na partida

# Criar Lógica de finalizar o client
# tecla "X" é clicada
# opção sair do jogo no menu principal é acionado

# Interações do usuário
# minimizar, ampliar e fechar tela
# opções de menu e pause durante o jogo
# comandos básicos

import pygame

pygame.init()
pygame.display.set_caption("Treasure Rush")
cell_size = 32  
grid_size = 16
width, height = cell_size * grid_size, cell_size * grid_size
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Cores (RGB)
black_color = (0, 0, 0)
white_color = (255, 255, 255)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
blue_color= (0, 0, 255)
background_color = (175, 196, 230)
wall_color = (128, 99, 69)
border_color = (210, 210, 210)

# Mapa Principal
main_map = [[0 for _ in range(16)] for _ in range(16)]
for i in range(16):
    for j in range(16):
        if i == 0 or j == 0 or i == 15 or j == 15:
            main_map[i][j] = 1
    
def draw_map():
    for i in range(grid_size):
        for j in range(grid_size):
            color = wall_color if main_map[i][j] == 1 else background_color
            border = wall_color if main_map[i][j] == 1 else border_color
            
            x = i * cell_size
            y = j * cell_size
            pygame.draw.rect(
                    screen,
                    color,
                    (j * cell_size, i * cell_size, cell_size, cell_size),
                )
            pygame.draw.rect(
                    screen,
                    border,
                    (j * cell_size, i * cell_size, cell_size, cell_size),
                    1
                )
            
def draw_player(player_position):
    row, col = player_position
    pygame.draw.rect(
        screen,
        black_color,
        (col * cell_size, row * cell_size, cell_size, cell_size)
    )

def run_game():
    game_over = False
    
    draw_map()
    draw_player([7, 7])
    
    while not game_over:

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                draw_player([8,7])
            
            if event.type == pygame.QUIT:
                game_over = True

run_game()
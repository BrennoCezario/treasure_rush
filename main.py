import pygame
import time
import random

# Constantes
cell_size = 32
grid_size_main = 16
grid_size_secondary = 8
info_bar_height = 50
screen_width = grid_size_main * cell_size
screen_height = grid_size_main * cell_size + info_bar_height

# Variáveis Globais
game_over = False
score = 0
start_time = time.time()
in_secondary_map = False  # Controla se o jogador está no mapa secundário


class Player:
    def __init__(self) -> None:
        self.reset_position()
        self.position = pygame.Rect(7 * cell_size + cell_size // 4,
                                    7 * cell_size + cell_size // 4 + info_bar_height, 
                                    cell_size // 2, cell_size // 2)

    def reset_position(self, secondary_map=False):
        """Define a posição inicial do jogador com base no mapa ativo."""
        self.grid_x = 7 if not secondary_map else 3
        self.grid_y = 7 if not secondary_map else 3

    def move(self, dx, dy, main_map):
        """Move o jogador no mapa ativo."""
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy

        # Verifica colisões com paredes
        if not main_map.is_wall(new_grid_y, new_grid_x):
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y

    def draw_player(self, screen, main_map):
        """Desenha o jogador na posição correta no mapa."""
        x = main_map.offset_x + self.grid_x * cell_size + cell_size // 4
        y = main_map.offset_y + self.grid_y * cell_size + cell_size // 4
        pygame.draw.rect(screen, "white", (x, y, cell_size // 2, cell_size // 2))


class MainMap:
    def __init__(self, grid_size, is_secondary=False) -> None:
        self.grid_size = grid_size
        self.space = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.is_secondary = is_secondary
        self.portal = None
        self.offset_x = (screen_width - grid_size * cell_size) // 2 if is_secondary else 0
        self.offset_y = info_bar_height + (screen_height - grid_size * cell_size - info_bar_height) // 2 if is_secondary else info_bar_height

        # Cria bordas e portal
        self.create_walls()
        self.create_portal()

    def create_walls(self):
        """Cria as bordas do mapa como paredes."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i == 0 or j == 0 or i == self.grid_size - 1 or j == self.grid_size - 1:
                    self.space[i][j] = 1

    def create_portal(self):
        """Adiciona um portal no centro do mapa."""
        center_x, center_y = self.grid_size // 2, self.grid_size // 2
        self.space[center_y][center_x] = 2
        color = "green" if self.is_secondary else "blue"
        self.portal = pygame.Rect(self.offset_x + center_x * cell_size + cell_size // 4,
                                  self.offset_y + center_y * cell_size + cell_size // 4,
                                  cell_size // 2, cell_size // 2)

    def draw_map(self, screen):
        """Desenha o mapa na tela."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = self.offset_x + j * cell_size
                y = self.offset_y + i * cell_size

                if self.space[i][j] == 1:
                    color = (150, 120, 70)
                    border = (100, 80, 50)
                elif self.space[i][j] == 2:
                    color = (50, 205, 50) if self.is_secondary else (70, 130, 180)  # Verde ou azul
                    border = (0, 150, 0) if self.is_secondary else (30, 100, 150)
                else:
                    color = (200, 180, 100)
                    border = (170, 150, 90)

                pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
                pygame.draw.rect(screen, border, (x, y, cell_size, cell_size), 1)

        # Desenha o portal
        if self.portal:
            pygame.draw.rect(screen, "green" if self.is_secondary else "blue", self.portal)

    def is_wall(self, row, col):
        """Verifica se uma posição específica é uma parede."""
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return self.space[row][col] == 1
        return True

class Treasure:
    def __init__(self):
        self.treasure_colors = ["violet", "green", "pink"]
        self.treasures = []  # Lista de tesouros (posição e cor)

    def generate_treasures(self):
        """Gera 8 tesouros aleatórios no mapa."""
        for _ in range(8):
            while True:
                x = random.randint(1, grid_size_main - 2)
                y = random.randint(1, grid_size_main - 2)
                position = (x, y)

                # Evita que o tesouro seja gerado em uma posição duplicada
                if position not in [treasure[0] for treasure in self.treasures]:
                    break

            color = random.choice(self.treasure_colors)
            self.treasures.append((position, color))

    def draw_treasures(self, screen):
        """Desenha os tesouros no mapa."""
        for (x, y), color in self.treasures:
            position = pygame.Rect(cell_size * x + cell_size // 4,
                                   cell_size * y + cell_size // 4 + info_bar_height,
                                   cell_size // 2, cell_size // 2)
            pygame.draw.rect(screen, color, position)

    def check_collision(self, player):
        """Verifica se o jogador pegou algum tesouro."""
        global score
        new_treasures = []
        for (x, y), color in self.treasures:
            treasure_rect = pygame.Rect(cell_size * x + cell_size // 4,
                                        cell_size * y + cell_size // 4 + info_bar_height,
                                        cell_size // 2, cell_size // 2)
            if player.position.colliderect(treasure_rect):
                score += 10  # Atualiza o placar
            else:
                new_treasures.append(((x, y), color))  # Mantém o tesouro
        self.treasures = new_treasures


def event_listener(player, main_map):
    """Gerencia os eventos de entrada do teclado."""
    global score, game_over, in_secondary_map
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                player.move(0, 1, main_map)
            if event.key in [pygame.K_UP, pygame.K_w]:
                player.move(0, -1, main_map)
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                player.move(-1, 0, main_map)
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                player.move(1, 0, main_map)

            score += 10

    # Detecta portal
    if main_map.portal and player.grid_x == main_map.grid_size // 2 and player.grid_y == main_map.grid_size // 2:
        in_secondary_map = not in_secondary_map
        player.reset_position(secondary_map=in_secondary_map)


def draw_info_bar(screen, score, elapsed_time):
    """Desenha a barra de informações."""
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)

    score_text = font.render(f"Placar: {score}", True, text_color)
    timer_text = font.render(f"Tempo: {elapsed_time:.1f}s", True, text_color)

    pygame.draw.rect(screen, (50, 50, 50), (0, 0, screen_width, info_bar_height))
    pygame.draw.line(screen, (255, 255, 255), (0, info_bar_height), (screen_width, info_bar_height), 2)

    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (screen_width - 200, 10))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Treasure Rush")

    player = Player()
    main_map = MainMap(grid_size_main)
    secondary_map = MainMap(grid_size_secondary, is_secondary=True)
    treasures = Treasure()
    treasures.generate_treasures()

    clock = pygame.time.Clock()

    while not game_over:
        elapsed_time = time.time() - start_time
        screen.fill("black")  # Preenche o fundo com preto

        # Alterna entre mapas
        if in_secondary_map:
            secondary_map.draw_map(screen)
            event_listener(player, secondary_map)
        else:
            main_map.draw_map(screen)
            treasures.draw_treasures(screen)  # Desenha os tesouros
            treasures.check_collision(player)
            event_listener(player, main_map)

        player.draw_player(screen, secondary_map if in_secondary_map else main_map)
        draw_info_bar(screen, score, elapsed_time)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

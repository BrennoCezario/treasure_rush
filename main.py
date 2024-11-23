import pygame

cell_size = 32
grid_size = 16  

game_over = False
  
class Player:
    def __init__(self) -> None:
        self.position = pygame.Rect(7*cell_size + cell_size // 4, 7*cell_size + cell_size // 4, grid_size, grid_size)
        
    def move(self, dx, dy, main_map):
        new_x = self.position.x + dx * cell_size
        new_y = self.position.y + dy * cell_size

        grid_x = new_x // cell_size
        grid_y = new_y // cell_size

        if not main_map.is_wall(grid_y, grid_x):
            self.position.x = new_x
            self.position.y = new_y
        
    def draw_player(self):
        pygame.draw.rect(surface= screen, color= "white", rect= self.position)


class MainMap:
    def __init__(self) -> None:
        self.space = [[0 for i in range(16)]for i in range(16)]
        for i in range(16):
            for j in range(16):
                if i == 0 or j == 0 or i == 15 or j == 15:
                    self.space[i][j] = 1 
                     
    def draw_map(self):
        for i in range(16):
            for j in range(16):
                color = (150, 120, 70) if self.space[i][j] == 1 else (200, 180, 100)
                border = (100, 80, 50) if self.space[i][j] == 1 else (170, 150, 90)
            
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
    def is_wall(self, row, col):
        return self.space[row][col] == 1

def event_listener(player, main_map):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global game_over
                game_over = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.move(0, 1, main_map)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.move(0, -1, main_map)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move(-1, 0, main_map)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move(1, 0, main_map)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((grid_size*cell_size, grid_size*cell_size))
    pygame.display.set_caption("Treasure Rush")

    player = Player()
    main_map = MainMap()
    
    while not game_over:
        event_listener(player, main_map)
        screen.fill("black")
        main_map.draw_map()
        player.draw_player()
        pygame.display.flip()
    
    pygame.quit()
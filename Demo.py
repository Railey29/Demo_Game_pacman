import pygame
import sys
import random 
# Initialize Pygame
pygame.init()


# Screen size
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pac-Man")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)



# Map grid: 0 = empty, 1 = wall, 2 = food
game_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,0,2,2,2,2,0,2,2,2,2,2,1],
    [1,2,1,1,0,1,1,1,1,0,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,0,1,1,1,1,0,1,1,0,1,2,1],
    [1,2,2,2,0,2,2,2,2,0,2,2,0,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

def move_ghost(x, y):
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x = x + dx
        new_y = y + dy
        if game_map[new_y][new_x] != 1:  # Bawal sa wall
            return new_x, new_y
    return x, y

def show_popup(message, color):
    font = pygame.font.SysFont(None, 60)
    text = font.render(message, True, color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def start_game():
    running = True
    # Player (Pac-Man)
    player_x = 1
    player_y = 1
    clock = pygame.time.Clock()
    ghost_timer = 0
    ghost_interval = 300 
    ghost_x, ghost_y = 14, 1
    pygame.mixer.init(frequency=16000)
    pygame.mixer.music.load("BG music.mp3")
    pygame.mixer.music.play()
    pygame.time.wait(1000)
    print("Successfully Play the BG music")

    while running:
        screen.fill(BLACK)
        # Draw map
        for y, row in enumerate(game_map):
            for x, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif tile == 2:
                    pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2), 5)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        if keys[pygame.K_LEFT]:
            new_x -= 1
        if keys[pygame.K_RIGHT]:
            new_x += 1
        if keys[pygame.K_UP]:
            new_y -= 1
        if keys[pygame.K_DOWN]:
            new_y += 1

        if game_map[new_y][new_x] != 1:
            player_x, player_y = new_x, new_y

        if game_map[player_y][player_x] == 2:
            game_map[player_y][player_x] = 0

        ghost_timer += clock.get_time()
        if ghost_timer >= ghost_interval:
            ghost_x, ghost_y = move_ghost(ghost_x, ghost_y)
            ghost_timer = 0

        # Draw player
        pygame.draw.circle(screen, YELLOW, 
            (player_x * TILE_SIZE + TILE_SIZE//2, player_y * TILE_SIZE + TILE_SIZE//2), 15)

        # Draw ghost
        pygame.draw.circle(screen, (255, 0, 255), 
            (ghost_x * TILE_SIZE + TILE_SIZE//2, ghost_y * TILE_SIZE + TILE_SIZE//2), 15)
        
        if not any(2 in row for row in game_map):
            show_popup("SUCCESS!", (0, 255, 0))
            pygame.mixer.init(frequency=16000)
            pygame.mixer.music.load("Success.mp3")
            pygame.mixer.music.play()
            pygame.time.wait(1000)
            running = False


        # Collision check
        if ghost_x == player_x and ghost_y == player_y:
            show_popup("GAME OVER!", (255, 0, 0))
            pygame.mixer.init(frequency=16000)
            pygame.mixer.music.load("Game Over.mp3")
            pygame.mixer.music.play()
            pygame.time.wait(1000)
            running = False
        

        pygame.display.flip()
        clock.tick(10)



start_game()
pygame.quit()
sys.exit()

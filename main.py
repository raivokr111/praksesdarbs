import random
import pygame

CELL = 20
COLS, ROWS = 32, 24
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
VISION = 4
FPS = 10
SNAKE_COLOR = "#50C878"
FOOD_COLOR = "#DC3C3C"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def random_cell(exclude):
    while True:
        cell = (random.randrange(COLS), random.randrange(ROWS))
        if cell not in exclude:
            return cell
def new_game():
    snake = [(COLS // 2, ROWS // 2)]
    return {
        "snake": snake,
        "dir": (1, 0),
        "food": random_cell(snake),
        "score": 0,
        "alive": True
    }
def visible(cell, head):
    dx = cell[0] - head[0]
    dy = cell[1] - head[1]
    return dx * dx + dy * dy <= VISION * VISION
def draw_cell(cell, color):
    pygame.draw.rect(screen, color, (cell[0] * CELL, cell[1] * CELL, CELL - 1, CELL - 1))
game = new_game()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            dx, dy = game["dir"]
            if event.key == pygame.K_UP and dy == 0:
                game["dir"] = (0, -1)
            elif event.key == pygame.K_DOWN and dy == 0:
                game["dir"] = (0, 1)
            elif event.key == pygame.K_LEFT and dx == 0:
                game["dir"] = (-1, 0)
            elif event.key == pygame.K_RIGHT and dx == 0:
                game["dir"] = (1, 0)
            elif event.key == pygame.K_SPACE and not game["alive"]:
                game = new_game()
    if game['alive']:
        head = game["snake"][0]
        new_head = (head[0] + game["dir"][0], head[1] + game["dir"][1])
        hit_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
        hit_self = new_head in game["snake"]
        if hit_wall or hit_self:
            game['alive'] = False
        else:
            game['snake'].insert(0, new_head)
            if new_head == game["food"]:
                game["score"] += 1
                game["food"] = random_cell(game["snake"])
            else:
                game['snake'].pop()
    screen.fill((0, 0, 0))
    head = game["snake"][0]

    for cell in game["snake"]:
        if visible(cell, head):
            draw_cell(cell, SNAKE_COLOR)
    if visible(game["food"], head):
        draw_cell(game["food"], FOOD_COLOR)

    screen.blit(font.render(f'Score: {game["score"]}', True, (255, 255, 255)), (10, 10))

    if not game["alive"]:
        msg = font.render("Game over - SPACE lai sāktu no jauna", True, (255, 255, 255))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
                    
import random
import pygame

CELL = 20
COLS, ROWS = 32, 24
HUD_HEIGHT = 40
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + HUD_HEIGHT
VISION = 4
FPS = 60
SPEED = 3
SNAKE_COLOR = "#50C878"
FOOD_COLOR = "#DC3C3C"
BG_COLOR = "#0B0F14"
HUD_COLOR = "#2D333B"
BORDER_COLOR = "#6E7681"
OUTSIDE_COLOR = "#000000" 

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
        "prev": list(snake),
        "progress": 0,
        "dir": (1, 0),
        "food": random_cell(snake),
        "score": 0,
        "alive": True,
        "start": pygame.time.get_ticks(),
        "elapsed": 0,
    }
def visible(cell, head):
    dx = cell[0] - head[0]
    dy = cell[1] - head[1]
    return dx * dx + dy * dy <= VISION * VISION + 0.01
def draw_cell(cell, color):
    pygame.draw.rect(screen, color, (cell[0] * CELL, cell[1] * CELL + HUD_HEIGHT, CELL - 1, CELL - 1))

def draw_smooth(cur, prev, t, color):
    x = (prev[0] + (cur[0] - prev[0]) * t) * CELL
    y = (prev[1] + (cur[1] - prev[1]) * t) * CELL + HUD_HEIGHT
    pygame.draw.rect(screen, color, (x, y, CELL - 1, CELL - 1))
    
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
    if game["alive"]:
        game["elapsed"] = pygame.time.get_ticks() - game["start"]
        game["progress"] += SPEED
        if game["progress"] >= CELL:
            game["progress"] = 0
            game["prev"] = list(game["snake"])
            head = game["snake"][0]
            new_head = (head[0] + game["dir"][0], head[1] + game["dir"][1])
            hit_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
            hit_self = new_head in game["snake"]
            if hit_wall or hit_self:
                game["alive"] = False
            else:
                game["snake"].insert(0, new_head)
                if new_head == game["food"]:
                    game["score"] += 1
                    game["food"] = random_cell(game["snake"])
                else:
                    game["snake"].pop()
    screen.fill(HUD_COLOR)
    pygame.draw.rect(screen, BG_COLOR, (0, HUD_HEIGHT, WIDTH, ROWS * CELL))

    t = game["progress"] / CELL if game["alive"] else 0
    snake = game["snake"]
    prev = game["prev"]
    hx = prev[0][0] + (snake[0][0] - prev[0][0]) * t
    hy = prev[0][1] + (snake[0][1] - prev[0][1]) * t

    for i, cell in enumerate(snake):
        old = prev[i] if i < len(prev) else prev[-1]
        draw_smooth(cell, old, t, SNAKE_COLOR)
    if visible(game["food"], (hx, hy)):
        draw_cell(game["food"], FOOD_COLOR)
    score_text = font.render(f'Score: {game["score"]}', True, (255, 255, 255))
    x = (WIDTH - score_text.get_width()) // 2
    y = (HUD_HEIGHT - score_text.get_height()) // 2
    screen.blit(score_text, (x, y))
    seconds = game["elapsed"] // 1000
    time_text = font.render(f'Time: {seconds // 60:02d}:{seconds % 60:02d}', True, (255, 255, 255))
    screen.blit(time_text, time_text.get_rect(midright=(WIDTH - 10, HUD_HEIGHT // 2)))

    if not game["alive"]:
        msg = font.render("Game over - SPACE lai sāktu no jauna", True, (255, 255, 255))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()         
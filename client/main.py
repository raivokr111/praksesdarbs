import pygame

from client.api_client import submit_score
from game.rules import (
    COLS, ROWS, new_game, set_direction, speed_factor, step, vision_radius, visible,
)

CELL = 20
HUD_HEIGHT = 40
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + HUD_HEIGHT
FPS = 60
SPEED = 3

SNAKE_COLOR = "#50C878"
FOOD_COLOR = "#DC3C3C"
BG_COLOR = "#0B0F14"
HUD_COLOR = "#2D333B"
BORDER_COLOR = "#6E7681"
TEXT_COLOR = "#E6EDF3"
HEAD_COLOR = "#C9FFD9"
TAIL_COLOR = "#1F6B3F"
EYE_COLOR = "#0B0F14"
FOOD_SHINE = "#FF9AA2"

POWERUP_INFO = {
    "light": ("Lukturis", "#FFD700"),
    "radar": ("Radars", "#4DA3FF"),
    "slow": ("Lēnums", "#B07CFF"),
    "double": ("Dubultpunkti", "#FF9F43"),
}

POWERUP_LETTERS = {
    "light": "L",
    "radar": "R",
    "slow": "S",
    "double": "x2",
}

DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def draw_cell(screen, cell, color):
    rect = (cell[0] * CELL, cell[1] * CELL + HUD_HEIGHT, CELL - 1, CELL - 1)
    pygame.draw.rect(screen, color, rect)


def draw_smooth(screen, cur, prev, t, color):
    x = (prev[0] + (cur[0] - prev[0]) * t) * CELL
    y = (prev[1] + (cur[1] - prev[1]) * t) * CELL + HUD_HEIGHT
    pygame.draw.rect(screen, color, (x, y, CELL - 1, CELL - 1), border_radius=6)
    return x, y

# cuskas izskats
def draw_eyes(screen, x, y, direction):
    cx = x + (CELL - 1) / 2
    cy = y + (CELL - 1) / 2
    dx, dy = direction
    px, py = -dy, dx
    for side in (1, -1):
        ex = cx + dx * 4 + px * 4 * side
        ey = cy + dy * 4 + py * 4 * side
        pygame.draw.circle(screen, EYE_COLOR, (ex, ey), 3)

def draw_snake(screen, snake, prev, t, direction):
    count = len(snake)
    head_pos = None
    for i in range(count - 1, -1, -1):
        old = prev[i] if i < len(prev) else prev[-1]
        if i == 0:
            color = HEAD_COLOR
        else:
            color = pygame.Color(SNAKE_COLOR).lerp(TAIL_COLOR, i / max(count - 1, 1))
        pos = draw_smooth(screen, snake[i], old, t, color)
        if i == 0:
            head_pos = pos
    draw_eyes(screen, head_pos[0], head_pos[1], direction)

def cell_center(cell):
    return cell[0] * CELL + CELL // 2, cell[1] * CELL + HUD_HEIGHT + CELL // 2

# ediens kas pulse
def draw_food(screen, cell, ticks):
    cx, cy = cell_center(cell)
    pygame.draw.circle(screen, FOOD_COLOR, (cx, cy), 8)
    pygame.draw.circle(screen, FOOD_SHINE, (cx - 3, cy - 3), 2)

# new powerup izskats
def draw_powerup(screen, tiny_font, cell, kind, ticks):
    cx, cy = cell_center(cell)
    color = POWERUP_INFO[kind][1]
    pygame.draw.circle(screen, color, (cx, cy), 9)
    text = tiny_font.render(POWERUP_LETTERS[kind], True, BG_COLOR)
    screen.blit(text, text.get_rect(center=(cx, cy)))

# rezultatu josla
def draw_hud(screen, font, score, elapsed):
    pygame.draw.rect(screen, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, score_text.get_rect(midleft=(10, HUD_HEIGHT // 2)))
    seconds = elapsed // 1000
    time_text = font.render(f"Time: {seconds // 60:02d}:{seconds % 60:02d}", True, TEXT_COLOR)
    screen.blit(time_text, time_text.get_rect(midright=(WIDTH - 10, HUD_HEIGHT // 2)))

# effektu josla
def draw_effects(screen, small_font, effects):
    x = 10
    for kind, steps_left in effects.items():
        name, color = POWERUP_INFO[kind]
        seconds = steps_left * CELL / (SPEED * FPS)
        text = small_font.render(f"{name} {seconds:.0f}s", True, color)
        screen.blit(text, (x, HUD_HEIGHT + 8))
        x += text.get_width() + 16

# pauzes ekrans
def draw_pause(screen, font):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((11, 15, 20, 230))
    screen.blit(overlay, (0, 0))
    lines = [
        ("Pauze", SNAKE_COLOR),
        ("ESC - turpināt", TEXT_COLOR),
        ("R - sākt no jauna", TEXT_COLOR),
        ("Q - iziet", TEXT_COLOR),
    ]
    y = HEIGHT // 2 - 70
    for text, color in lines:
        img = font.render(text, True, color)
        screen.blit(img, img.get_rect(center=(WIDTH // 2, y)))
        y += 45

# name input ekrans
def ask_name(screen, font, clock):
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 20 and event.unicode.isprintable():
                    name += event.unicode

        screen.fill(BG_COLOR)
        prompt = font.render("Ievadi vārdu un spied ENTER", True, TEXT_COLOR)
        typed = font.render(name + "_", True, SNAKE_COLOR)
        screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
        screen.blit(typed, typed.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        pygame.display.flip()
        clock.tick(30)

# main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blind Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    hud_font = pygame.font.SysFont("verdana", 28, bold=True)
    tiny_font = pygame.font.SysFont(None, 18, bold=True)

    player_name = ask_name(screen, font, clock)
    if player_name is None:
        pygame.quit()
        return

    game = new_game()
    progress = 0
    start = pygame.time.get_ticks()
    elapsed = 0
    sent = False
    paused = False
    pause_start = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                now = pygame.time.get_ticks()
                if event.key == pygame.K_ESCAPE and game["alive"]:
                    paused = not paused
                    if paused:
                        pause_start = now
                    else:
                        start += now - pause_start
                elif paused:
                    if event.key == pygame.K_r:
                        game = new_game()
                        progress, elapsed, sent = 0, 0, False
                        start = now
                        paused = False
                    elif event.key == pygame.K_q:
                        running = False
                elif event.key in DIRECTIONS:
                    set_direction(game, DIRECTIONS[event.key])
                elif event.key == pygame.K_SPACE and not game["alive"]:
                    game = new_game()
                    progress, elapsed, sent = 0, 0, False
                    start = now

        if game["alive"] and not paused:
            elapsed = pygame.time.get_ticks() - start
            progress += SPEED * speed_factor(game)
            if progress >= CELL:
                progress = 0
                step(game)
        elif not game["alive"] and not sent:
            sent = True
            submit_score(player_name, game["score"], elapsed // 1000)

        screen.fill(HUD_COLOR)
        pygame.draw.rect(screen, BG_COLOR, (0, HUD_HEIGHT, WIDTH, ROWS * CELL))

        t = progress / CELL if game["alive"] else 0
        snake, prev = game["snake"], game["prev"]
        hx = prev[0][0] + (snake[0][0] - prev[0][0]) * t
        hy = prev[0][1] + (snake[0][1] - prev[0][1]) * t

        draw_snake(screen, snake, prev, t, game["dir"])

        radius = vision_radius(game)
        ticks = pygame.time.get_ticks()
        for food in game["food"]:
            if visible(food, (hx, hy), radius):
                draw_food(screen, food, ticks)
        pu = game["powerup"]
        if pu and visible(pu["cell"], (hx, hy), radius):
            draw_powerup(screen, tiny_font, pu["cell"], pu["kind"], ticks)

        pygame.draw.rect(screen, BORDER_COLOR, (0, HUD_HEIGHT, WIDTH, ROWS * CELL), 3)
        draw_hud(screen, hud_font, game["score"], elapsed)
        draw_effects(screen, small_font, game["effects"])

        if not game["alive"]:
            msg = font.render("Game over - SPACE lai sāktu no jauna", True, TEXT_COLOR)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + HUD_HEIGHT // 2)))

        if paused:
            draw_pause(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
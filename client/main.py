import pygame

from client.api_client import submit_score
from game.rules import COLS, ROWS, new_game, set_direction, step, visible

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
    pygame.draw.rect(screen, color, (x, y, CELL - 1, CELL - 1))


def draw_hud(screen, font, score, elapsed):
    pygame.draw.rect(screen, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, score_text.get_rect(midleft=(10, HUD_HEIGHT // 2)))
    seconds = elapsed // 1000
    time_text = font.render(f"Time: {seconds // 60:02d}:{seconds % 60:02d}", True, TEXT_COLOR)
    screen.blit(time_text, time_text.get_rect(midright=(WIDTH - 10, HUD_HEIGHT // 2)))


def main():
    player_name = input("Ievadi vārdu: ").strip()[:20] or "Anonīms"
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blind Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    game = new_game()
    progress = 0
    start = pygame.time.get_ticks()
    elapsed = 0
    sent = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in DIRECTIONS:
                    set_direction(game, DIRECTIONS[event.key])
                elif event.key == pygame.K_SPACE and not game["alive"]:
                    game = new_game()
                    progress, elapsed, sent = 0, 0, False
                    start = pygame.time.get_ticks()

        if game["alive"]:
            elapsed = pygame.time.get_ticks() - start
            progress += SPEED
            if progress >= CELL:
                progress = 0
                step(game)
        elif not sent:
            sent = True
            submit_score(player_name, game["score"], elapsed // 1000)

        screen.fill(HUD_COLOR)
        pygame.draw.rect(screen, BG_COLOR, (0, HUD_HEIGHT, WIDTH, ROWS * CELL))

        t = progress / CELL if game["alive"] else 0
        snake, prev = game["snake"], game["prev"]
        hx = prev[0][0] + (snake[0][0] - prev[0][0]) * t
        hy = prev[0][1] + (snake[0][1] - prev[0][1]) * t

        for i, cell in enumerate(snake):
            old = prev[i] if i < len(prev) else prev[-1]
            draw_smooth(screen, cell, old, t, SNAKE_COLOR)
        if visible(game["food"], (hx, hy)):
            draw_cell(screen, game["food"], FOOD_COLOR)

        pygame.draw.rect(screen, BORDER_COLOR, (0, HUD_HEIGHT, WIDTH, ROWS * CELL), 3)
        draw_hud(screen, font, game["score"], elapsed)

        if not game["alive"]:
            msg = font.render("Game over - SPACE lai sāktu no jauna", True, TEXT_COLOR)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + HUD_HEIGHT // 2)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
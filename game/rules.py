import random

COLS, ROWS = 32, 24
VISION = 4


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
        "dir": (1, 0),
        "food": random_cell(snake),
        "score": 0,
        "alive": True,
    }


def set_direction(game, direction):
    if direction[0] + game["dir"][0] != 0 or direction[1] + game["dir"][1] != 0:
        game["dir"] = direction


def step(game):
    game["prev"] = list(game["snake"])
    head = game["snake"][0]
    new_head = (head[0] + game["dir"][0], head[1] + game["dir"][1])
    hit_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
    if hit_wall or new_head in game["snake"]:
        game["alive"] = False
        return
    game["snake"].insert(0, new_head)
    if new_head == game["food"]:
        game["score"] += 1
        game["food"] = random_cell(game["snake"])
    else:
        game["snake"].pop()


def visible(cell, head, radius=VISION):
    dx = cell[0] - head[0]
    dy = cell[1] - head[1]
    return dx * dx + dy * dy <= radius * radius + 0.01
import random

COLS, ROWS = 32, 24
VISION = 4
LIGHT_VISION = 8
RADAR_VISION = 99
FOOD_COUNT = 2
POWERUP_CHANCE = 0.8
POWERUP_RANDOM = 0.01 
POWERUP_LIFETIME = 100
POWERUP_STEPS = {
    "light": 90,
    "radar": 25,
    "slow": 70,
    "double": 90,
}

def occupied(game):
    cells = list(game["snake"]) + list(game['food'])
    if game ['powerup']:
        cells.append(game['powerup']['cell'])
    return cells

def random_cell(exclude):
    while True:
        cell = (random.randrange(COLS), random.randrange(ROWS))
        if cell not in exclude:
            return cell


def new_game():
    snake = [(COLS // 2, ROWS // 2)]
    game = {
        "snake": snake,
        "prev": list(snake),
        "dir": (1, 0),
        "queue": [],
        "food": [],
        "powerup": None,
        "effects": {}, 
        "score": 0,
        "alive": True,
    }
    while len(game['food']) < FOOD_COUNT:
        game['food'].append(random_cell(occupied(game)))
    return game

def set_direction(game, direction):
    last = game["queue"][-1] if game["queue"] else game["dir"]
    if direction == last:
        return
    if direction[0] + last[0] == 0 and direction[1] + last[1] == 0:
        return
    if len(game["queue"]) < 2:
        game["queue"].append(direction)

def spawn_powerup(game):
    game ["powerup"] = {
        "kind": random.choice(list(POWERUP_STEPS)),
        "cell": random_cell(occupied(game)),
        "ttl": POWERUP_LIFETIME,
    }

def tick_timers(game):
    for kind in list(game["effects"]):
        game["effects"][kind] -= 1
        if game["effects"][kind] <= 0:
            del game["effects"][kind]
    if game ["powerup"]:
        game["powerup"]["ttl"] -= 1
        if game["powerup"]["ttl"] <= 0:
            game["powerup"] = None


def step(game):
    if game["queue"]:
        game["dir"] = game["queue"].pop(0)
    game["prev"] = list(game["snake"])
    head = game["snake"][0]
    new_head = (head[0] + game["dir"][0], head[1] + game["dir"][1])
    hit_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
    if hit_wall or new_head in game["snake"]:
        game["alive"] = False
        return

    game["snake"].insert(0, new_head)
    if new_head in game["food"]:
        game["food"].remove(new_head)
        game["score"] += 2 if "double" in game["effects"] else 1
        game["food"].append(random_cell(occupied(game)))
        if game["powerup"] is None and random.random() < POWERUP_CHANCE:
            spawn_powerup(game)
    else:
        game["snake"].pop()

    pu = game["powerup"]
    if pu and pu["cell"] == new_head:
        game["effects"][pu["kind"]] = POWERUP_STEPS[pu["kind"]]
        game["score"] += 1
        game["powerup"] = None

    if game["powerup"] is None and random.random() < POWERUP_RANDOM:
        spawn_powerup(game)

    tick_timers(game)

def vision_radius(game):
    if "radar" in game["effects"]:
        return RADAR_VISION
    elif "light" in game["effects"]:
        return LIGHT_VISION
    return VISION

def speed_factor(game):
    return 0.5 if "slow" in game["effects"] else 1.0

def visible(cell, head, radius=VISION):
    dx = cell[0] - head[0]
    dy = cell[1] - head[1]
    return dx * dx + dy * dy <= radius * radius + 0.01
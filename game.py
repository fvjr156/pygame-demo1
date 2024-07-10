import pygame
import sys

pygame.init()

TITLE = "Demo Game"
WIDTH = 400
HEIGHT = 300
TILE_SIZE = 20
FPS = 60

tiles = {
    "00": pygame.image.load("images/tile_00.png"),
    "01": pygame.image.load("images/tile_01.png"),
    "02": pygame.image.load("images/tile_02.png"),
    "03": pygame.image.load("images/tile_03.png"),
    "0A": pygame.image.load("images/tile_0a.png"),
    "A1": pygame.image.load("images/tile_a1.png"),
    "A2": pygame.image.load("images/tile_a2.png"),
    "A3": pygame.image.load("images/tile_a3.png"),
    "A4": pygame.image.load("images/tile_a4.png"),
    "A5": pygame.image.load("images/tile_a5.png"),
    "A6": pygame.image.load("images/tile_a6.png"),
    "B0": pygame.image.load("images/tile_b0.png"),
    "B1": pygame.image.load("images/tile_b1.png"),
    "B2": pygame.image.load("images/tile_b2.png"),
    "B3": pygame.image.load("images/tile_b3.png"),
    "B4": pygame.image.load("images/tile_b4.png"),
    "B5": pygame.image.load("images/tile_b5.png"),
    "B6": pygame.image.load("images/tile_b6.png"),
    "B7": pygame.image.load("images/tile_b7.png"),
    "B8": pygame.image.load("images/tile_b8.png"),
}

class PlayerSprite:
    def __init__(self, idle, walk1, walk2):
        self.idle = idle
        self.walk1 = walk1
        self.walk2 = walk2

player0 = PlayerSprite(
    pygame.image.load("images/sprite0.png"),
    pygame.image.load("images/sprite0_walk1.png"),
    pygame.image.load("images/sprite0_walk2.png"),
)

def load_map_from_file(filename):
    with open(filename, "r") as f:
        return [line.strip().split() for line in f.readlines()]

tile_map = load_map_from_file("map_0.txt")
collision_map = load_map_from_file("collision_0.txt")

player = pygame.Rect(100, 20, 27, 32)
player_image = player0.idle

walking = False
walk_frame = 0
walk_timer = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

def is_passable(rect):
    corners = [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.left, rect.bottom),
        (rect.right, rect.bottom)
    ]
    for x, y in corners:
        col = int(x // TILE_SIZE)
        row = int(y // TILE_SIZE)
        if col < 0 or col >= len(collision_map[0]) or row < 0 or row >= len(collision_map):
            return False
        if collision_map[row][col] != "00":
            return False
    return True

def update_camera(player, camera, screen_width, screen_height, map_width, map_height):
    camera.x = player.x + player.width // 2 - screen_width // 2
    camera.y = player.y + player.height // 2 - screen_height // 2
    
    camera.x = max(0, min(camera.x, map_width - screen_width))
    camera.y = max(0, min(camera.y, map_height - screen_height))

camera = pygame.Rect(0, 0, WIDTH, HEIGHT)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    walking = False

    if keys[pygame.K_LEFT] and player.left > 0 and is_passable(player.move(-2, 0)):
        player.x -= 2
        walking = True
    if keys[pygame.K_RIGHT] and player.right < len(tile_map[0]) * TILE_SIZE and is_passable(player.move(2, 0)):
        player.x += 2
        walking = True
    if keys[pygame.K_UP] and player.top > 0 and is_passable(player.move(0, -2)):
        player.y -= 2
        walking = True
    if keys[pygame.K_DOWN] and player.bottom < len(tile_map) * TILE_SIZE and is_passable(player.move(0, 2)):
        player.y += 2
        walking = True

    if walking:
        walk_timer += 1
        if walk_timer % 10 == 0:
            walk_frame = (walk_frame + 1) % 2
        player_image = player0.walk1 if walk_frame == 0 else player0.walk2
    else:
        player_image = player0.idle

    update_camera(player, camera, WIDTH, HEIGHT, len(tile_map[0]) * TILE_SIZE, len(tile_map) * TILE_SIZE)

    screen.fill((0, 0, 0))
    for y, row in enumerate(tile_map):
        for x, tile_id in enumerate(row):
            screen.blit(tiles[tile_id], (x * TILE_SIZE - camera.x, y * TILE_SIZE - camera.y))
    screen.blit(player_image, (player.x - camera.x, player.y - camera.y))

    pygame.display.flip()
    clock.tick(FPS)

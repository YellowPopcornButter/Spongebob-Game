import pygame
import random
import math

# --- Constants ---
WIDTH, HEIGHT = 700, 700
FPS = 60

# --- Colors ---
BLUE = (162, 223, 229)
GRAY = (198, 198, 198)
WHITE = (255, 255, 255)
PINK = (255, 134, 134)
PROGRESS_COLOR = (94, 163, 245)

# --- Platform Drawing ---
def draw_platform(x, y):
    pygame.draw.rect(win, (160, 105, 60), (x, y, 90, 10))
    pygame.draw.rect(win, (106, 61, 23), (x, y, 90, 10), 2)

# --- Pygame Init ---
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spongebob Burger Game")
clock = pygame.time.Clock()

# --- Global Variables ---
items_count = 0
range_collect = 20
amount = 5
completion_width = 147
health_width = 147
xpos, ypos = 0, 0
radius = 35
gravity = 0.1
velocity = 0
lift = -5

# --- Bubble Class ---
class Bubble:
    def __init__(self, color, speed, size):
        self.color = color
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.y_speed = speed
        if size == 10:
            self.radius = random.randint(10, 20)
        elif size == 20:
            self.radius = random.randint(21, 30)
        else:
            self.radius = random.randint(31, 40)

    def draw(self):
        bubble_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(bubble_surface, (255, 255, 255, 100), (self.radius, self.radius), self.radius)
        win.blit(bubble_surface, (int(self.x - self.radius), int(self.y - self.radius)))

    def descend(self):
        self.y -= self.y_speed
        if self.y < 0:
            self.y = HEIGHT

# --- Ingredient Class ---
class Ingredient:
    def __init__(self, color):
        self.color = color
        self.original_color = color
        self.x = random.randint(50, 550)
        self.y = random.randint(50, 550)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, 30, 8))
        pygame.draw.rect(win, self.color, (self.x, self.y+8, 30, 8))

    def collect(self):
        self.color = GRAY

    def pos(self):
        return self.x, self.y

# --- Player Class ---
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 35
        self.gravity = 0.1
        self.velocity = 0

    def draw(self):
        pygame.draw.rect(win, (255, 211, 121), (self.x, self.y, self.radius, self.radius))
        pygame.draw.rect(win, (158, 91, 47), (self.x, self.y + 30, self.radius, 11))
        pygame.draw.rect(win, WHITE, (self.x, self.y + 28, self.radius, 5))
        pygame.draw.rect(win, (255, 0, 0), (self.x + 14, self.y + 28, 8, 5))
        pygame.draw.circle(win, WHITE, (int(self.x + 10), int(self.y + 10)), 7)
        pygame.draw.circle(win, WHITE, (int(self.x + 26), int(self.y + 10)), 7)
        pygame.draw.circle(win, (83, 138, 148), (int(self.x + 10), int(self.y + 10)), 5)
        pygame.draw.circle(win, (83, 138, 148), (int(self.x + 26), int(self.y + 10)), 5)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5

        self.velocity += self.gravity
        self.y += self.velocity

        on_platform = False
        for px, py in platform_coords:
            if (self.x + self.radius > px and self.x < px + 90) and (self.y + self.radius >= py and self.y + self.radius <= py + 10):
                self.y = py - self.radius
                self.velocity = 0
                on_platform = True

        if not on_platform:
            if self.y > HEIGHT - self.radius:
                self.y = HEIGHT - self.radius
                self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius

    def jump(self):
        self.velocity += lift

    def pos(self):
        return self.x, self.y

# --- Pineapple Drawing ---
def draw_pineapple():
    pygame.draw.rect(win, (255, 231, 178), (0, 380, HEIGHT, 400))
    pygame.draw.ellipse(win, (247, 173, 52), (75, 100, 250, 300))

    leaf_color = (98, 203, 53)
    leaf_points = [
        (80,30), (235,105), (185,100),
        (55,63), (235,105), (185,100),
        (65,55), (235,105), (185,100),
        (110,60), (235,105), (185,100),
        (115,30), (235,105), (185,100),
        (145,30), (235,105), (185,100),
        (175,30), (235,105), (185,100),
        (200,30), (235,105), (185,100),
        (225,30), (235,105), (185,100),
        (175,30), (235,105), (185,100),
        (255,30), (235,105), (185,100),
        (175,30), (235,105), (185,100),
        (285,30), (235,105), (185,100),
        (255,60), (235,105), (185,100),
        (260,55), (235,105), (185,100),
        (335,63), (235,105), (185,100),
        (345,63), (235,105), (185,100),
        (320,30), (235,105), (185,100)
    ]
    for i in range(0, len(leaf_points), 3):
        pygame.draw.polygon(win, leaf_color, [leaf_points[i], leaf_points[i+1], leaf_points[i+2]])

    pygame.draw.line(win, (216, 88, 24), (210, 105), (75, 235), 3)
    pygame.draw.line(win, (216, 88, 24), (260, 120), (80, 295), 3)
    pygame.draw.line(win, (216, 88, 24), (295, 155), (105, 345), 3)
    pygame.draw.line(win, (216, 88, 24), (320, 215), (150, 385), 3)
    pygame.draw.line(win, (216, 88, 24), (85, 200), (215, 395), 3)
    pygame.draw.line(win, (216, 88, 24), (120, 135), (280, 365), 3)
    pygame.draw.line(win, (216, 88, 24), (180, 100), (315, 300), 3)

    pygame.draw.ellipse(win, (24, 176, 216), (110, 185, 60, 60))
    pygame.draw.ellipse(win, (168, 229, 245), (122, 197, 35, 35))

    pygame.draw.ellipse(win, (24, 176, 216), (230, 275, 60, 60))
    pygame.draw.ellipse(win, (168, 229, 245), (242, 287, 35, 35))

    pygame.draw.ellipse(win, (24, 176, 216), (170, 300, 60, 100))

# --- Draw Spikes ---
def draw_spikes():
    spike_y = HEIGHT - 40
    spike_width = 20
    spike_height = 40
    num_spikes = WIDTH // spike_width
    for i in range(num_spikes):
        points = [
            (i * spike_width, spike_y + spike_height),
            (i * spike_width + spike_width / 2, spike_y),
            (i * spike_width + spike_width, spike_y + spike_height)
        ]
        pygame.draw.polygon(win, (0, 0, 0), points)

# --- Check Spike Collision ---
def check_spike_collision(player):
    spike_y = HEIGHT - 40
    if player.y + player.radius > spike_y:
        if 0 <= player.x <= WIDTH:
            return True
    return False

# --- Game Over screen ---
def draw_game_over():
    win.fill((234, 220, 104))
    font_big = pygame.font.SysFont("arial", 50, bold=True)
    font_small = pygame.font.SysFont("arial", 25)
    win.blit(font_big.render("Game Over!", True, (106, 29, 7)), (WIDTH//2 - 130, HEIGHT//2 - 40))
    win.blit(font_small.render("Please restart to play again", True, (106, 29, 7)), (WIDTH//2 - 140, HEIGHT//2 + 20))
    pygame.display.flip()

# --- Win screen ---
def draw_win_screen():
    win.fill((189, 255, 160))
    font_big = pygame.font.SysFont("arial", 50, bold=True)
    font_small = pygame.font.SysFont("arial", 25)
    win.blit(font_big.render("You Win!", True, (34, 139, 34)), (WIDTH//2 - 100, HEIGHT//2 - 40))
    win.blit(font_small.render("Please restart to play again", True, (34, 139, 34)), (WIDTH//2 - 140, HEIGHT//2 + 20))
    pygame.display.flip()

# --- Setup Game Objects ---
player = Player()
ingredients = [
    Ingredient((252, 211, 156)),
    Ingredient((240, 93, 56)),
    Ingredient((121, 245, 94)),
    Ingredient((160, 56, 27)),
    Ingredient((255, 233, 103)),
    Ingredient((160, 198, 78)),
    Ingredient((234, 140, 179))
]
bubbles = [
    Bubble(BLUE, 0.5, 10) for _ in range(amount)
] + [
    Bubble(BLUE, 1.2, 20) for _ in range(amount)
] + [
    Bubble(BLUE, 2, 30) for _ in range(amount)
]

platform_coords = [
    (85, 85),
    (600, 300),
    (WIDTH - 200, HEIGHT - 200),
    (WIDTH // 2, HEIGHT // 2),
    (100, HEIGHT - 315),
    (245, 200),
    (WIDTH // 2 - 100, HEIGHT - 200)
]

# --- Main Loop ---
running = True
game_over = False

while running:
    clock.tick(FPS)

    if health_width <= 0:
        game_over = True
        draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        continue

    if completion_width <= 1:  # ← allows the win screen to trigger even if it's slightly above 0
        game_over = True
        draw_win_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        continue

    win.fill(BLUE)
    draw_pineapple()

    for plat in platform_coords:
        draw_platform(*plat)

    draw_spikes()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)

    if check_spike_collision(player):
        health_width -= 1
        if health_width < 0:
            health_width = 0

    for b in bubbles:
        b.draw()
        b.descend()

    px, py = player.pos()
    for ing in ingredients:
        ix, iy = ing.pos()
        if math.hypot(px - ix, py - iy) < range_collect:
            if ing.color != GRAY:
                ing.collect()
                items_count += 1
                completion_width -= 150 // 7
        ing.draw()

    player.draw()

    pygame.draw.rect(win, GRAY, (WIDTH - 170, 20, 150, 30))
    pygame.draw.rect(win, PINK, (WIDTH - 170, 20, health_width, 30))

    pygame.draw.rect(win, GRAY, (WIDTH - 170, 60, 150, 30))
    pygame.draw.rect(win, PROGRESS_COLOR, (WIDTH - 170, 60, completion_width, 30))

    pygame.display.flip()

pygame.quit()

import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
FPS = 60

NUM_SQUARES = 20
MIN_SIZE = 10
MAX_SIZE = 50
GLOBAL_MAX_SPEED = 5.0
DIRECTION_JITTER_CHANCE_PER_SECOND = 2.0
MAX_DIRECTION_JITTER_DEGREES = 15.0
THREAT_RADIUS = 80.0
HUNT_RADIUS = 120.0
SPAWN_INTERVAL = 3.0


Square = dict[str, float | tuple[int, int, int]]


def create_square(size: float = None) -> Square:
    size = random.randint(MIN_SIZE, MAX_SIZE)
    max_speed = GLOBAL_MAX_SPEED * (MIN_SIZE / size)
    speed = random.uniform(0.5, max_speed)
    angle = random.uniform(0, 2 * math.pi)
    return {
        "x": float(random.randint(0, WIDTH - size)),
        "y": float(random.randint(0, HEIGHT - size)),
        "vx": speed * math.cos(angle),
        "vy": speed * math.sin(angle),
        "size": float(size),
        "max_speed": max_speed,
        "color": (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
        "dead": 0.0,
        "life": float(random.uniform(30.0, 180.0)),
    }

def init_squares() -> list[Square]:
    squares = []    
    
    for _ in range(5):
        squares.append(create_square(25.0))
    for _ in range(10):
        squares.append(create_square(10.0))
    for _ in range(30):
        squares.append(create_square(4.0))
        
    return squares

def apply_random_direction_jitter(square: Square, vx: float, vy: float, dt_seconds: float) -> tuple[float, float]:
    jitter_probability = min(1.0, DIRECTION_JITTER_CHANCE_PER_SECOND * dt_seconds)
    if random.random() >= jitter_probability:
        return vx, vy

    speed = math.hypot(vx, vy)
    if speed <= 0.0:
        return vx, vy

    angle = math.atan2(vy, vx)
    jitter_degrees = random.uniform(-MAX_DIRECTION_JITTER_DEGREES, MAX_DIRECTION_JITTER_DEGREES)
    new_angle = angle + math.radians(jitter_degrees)
    new_vx = speed * math.cos(new_angle)
    new_vy = speed * math.sin(new_angle)

    max_speed = float(square["max_speed"])
    current_speed = math.hypot(new_vx, new_vy)
    if current_speed > max_speed:
        scale = max_speed / current_speed
        new_vx *= scale
        new_vy *= scale

    return new_vx, new_vy


def rects_overlap(ax: float, ay: float, as_: float, bx: float, by: float, bs: float) -> bool:
    return ax < bx + bs and ax + as_ > bx and ay < by + bs and ay + as_ > by


def update_square(square: Square, all_squares: list[Square], dt_seconds: float) -> None:
    vx = float(square["vx"])
    vy = float(square["vy"])
    size = float(square["size"])
    x = float(square["x"]) + vx
    y = float(square["y"]) + vy
    vx, vy = apply_random_direction_jitter(square, vx, vy, dt_seconds)
    closest_threat = None
    closest_prey = None
    min_threat_dist = THREAT_RADIUS
    min_prey_dist = HUNT_RADIUS

    for other in all_squares:
        if other is square:
            continue
        other_size = float(other["size"])
        dx = float(other["x"]) - x
        dy = float(other["y"]) - y
        dist = math.hypot(dx, dy)

        if other_size > size and dist < min_threat_dist:
            min_threat_dist = dist
            closest_threat = (-dx, -dy)

        elif other_size < size and dist < min_prey_dist:
            min_prey_dist = dist
            closest_prey = (dx, dy, other)

    if closest_threat:
        dx, dy = closest_threat
        dist = math.hypot(dx, dy)
        if dist > 0:
            target_vx = (dx / dist) * float(square["max_speed"])
            target_vy = (dy / dist) * float(square["max_speed"])
            vx += (target_vx - vx) * 0.15
            vy += (target_vy - vy) * 0.15
    elif closest_prey:
        dx, dy, prey = closest_prey
        dist = math.hypot(dx, dy)
        if dist > 0:
            target_vx = (dx / dist) * float(square["max_speed"])
            target_vy = (dy / dist) * float(square["max_speed"])
            vx += (target_vx - vx) * 0.08
            vy += (target_vy - vy) * 0.08

    x += vx
    y += vy

    if x > WIDTH:
        x = -size 
    elif x < -size:
        x = float(WIDTH) 

    if y > HEIGHT:
        y = -size  
    elif y < -size:
        y = float(HEIGHT)

    square["x"] = x
    square["y"] = y
    square["vx"] = vx
    square["vy"] = vy
    square["life"] = float(square["life"]) - dt_seconds
def check_kills(squares: list[Square]) -> set[int]:
    killed = set()
    for i, a in enumerate(squares):
        if i in killed:
            continue
        for j, b in enumerate(squares):
            if j <= i or j in killed:
                continue
            a_size = float(a["size"])
            b_size = float(b["size"])
            if a_size == b_size:
                continue
            if rects_overlap(float(a["x"]), float(a["y"]), a_size, float(b["x"]), float(b["y"]), b_size):
                if a_size > b_size:
                    killed.add(j)
                else:
                    killed.add(i)
    return killed


def draw_square(screen: pygame.Surface, square: Square) -> None:
    x = int(square["x"])
    y = int(square["y"])
    size = int(square["size"])
    color = square["color"]
    pygame.draw.rect(screen, color, (x, y, size, size))


def main() -> None:
    pygame.init()
    font = pygame.font.SysFont("Serif", 18)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares")
    clock = pygame.time.Clock()

    squares = init_squares()
    spawn_timer = 0.0
    running = True

    while running:
        dt = clock.tick(FPS)
        dt_seconds = dt / 1000.0
        spawn_timer += dt_seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for square in squares:
            update_square(square, squares, dt_seconds)

        killed = check_kills(squares)
        new_squares = []
        for i, s in enumerate(squares):
            if i in killed or s["life"] <= 0:
                new_squares.append(create_square(s["size"]))
            else:
                new_squares.append(s)

        squares = new_squares
        if spawn_timer >= SPAWN_INTERVAL:
            spawn_timer = 0.0
            squares.append(create_square())

        screen.fill((15, 15, 15))
        fps_text = font.render(f"FPS: {clock.get_fps():.1f}  alive: {len(squares)}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        for square in squares:
            draw_square(screen, square)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
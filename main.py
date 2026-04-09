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


Square = dict[str, float | tuple[int, int, int]]


def create_square() -> Square:
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
    }


def init_squares() -> list[Square]:
    return [create_square() for _ in range(NUM_SQUARES)]


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


def update_square(square: Square, all_squares: list[Square], dt_seconds: float) -> None:
    vx = float(square["vx"])
    vy = float(square["vy"])
    size = float(square["size"])
    x = float(square["x"]) + vx
    y = float(square["y"]) + vy

    closest_threat = None
    min_dist = THREAT_RADIUS

    for other in all_squares:
        if other is square: continue
        if float(other["size"]) > size:
            dx = x - float(other["x"])
            dy = y - float(other["y"])
            dist = math.hypot(dx, dy)
            if dist < min_dist:
                min_dist = dist
                closest_threat = (dx, dy)
    if closest_threat:
        dx, dy = closest_threat
        if min_dist > 0:
            target_vx = (dx / min_dist) * float(square["max_speed"])
            target_vy = (dy / min_dist) * float(square["max_speed"])
            vx += (target_vx - vx) * 0.1 
            vy += (target_vy - vy) * 0.1
    else:
        vx, vy = apply_random_direction_jitter(square, vx, vy, dt_seconds)

    x += vx
    y += vy

    if x < 0:
        x = 0
        vx = abs(vx)
    elif x + size > WIDTH:
        x = float(WIDTH - size)
        vx = -abs(vx)

    if y < 0:
        y = 0
        vy = abs(vy)
    elif y + size > HEIGHT:
        y = float(HEIGHT - size)
        vy = -abs(vy)

    square["x"] = x
    square["y"] = y
    square["vx"] = vx
    square["vy"] = vy


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
    running = True

    while running:
        dt = clock.tick(FPS)
        dt_seconds = dt / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for square in squares:
            update_square(square, squares, dt_seconds)

        screen.fill((15, 15, 15))

        fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        for square in squares:
            draw_square(screen, square)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

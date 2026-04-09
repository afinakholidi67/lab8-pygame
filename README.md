# lab8-pygame

PyGame application — 100 squares moving randomly on screen.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Features

- 100 squares with random sizes, colors, and velocities
- Max speed inversely proportional to square size (bigger = slower)
- Direction jitter: squares gradually change direction over time
- Border bouncing

## Data Structure

Each square is a `dict[str, float | tuple[int, int, int]]`.

Keys: `x`, `y`, `vx`, `vy`, `size`, `max_speed`, `color`.

Chose dict over tuple for named access. Chose dict over class to keep things simple — no behavior needed beyond external functions.

## Rendering Loop

1. `screen.fill()` — clears back buffer
1. Draw all squares
1. `pygame.display.flip()` — swaps buffers (double buffering, flicker-free)
1. `clock.tick(60)` — caps loop at 60 fps, sleeps if frame finished early

## Max Speed = f(size)

Formula: `max_speed = GLOBAL_MAX_SPEED * (MIN_SIZE / size)`

Bigger squares get lower max speed. Capped at `GLOBAL_MAX_SPEED`.

## Jitter

Each frame, with probability `JITTER_CHANCE * dt`, rotate the velocity vector by a small random angle. Speed magnitude is preserved by construction (rotation is rigid). A clamp guard handles edge cases where speed already exceeds max.

## THREAT_RADIUS

Added `THREAT_RADIUS = 80.0` at the top — controls how close a bigger square has to be before a smaller one starts fleeing. Value is in pixels. The higher it is, the earlier small squares start running. Too high and they’ll be stuck in corners constantly.

## NUM_SQUARES

Reduced from 100 to 20 as required by the task.

## Threat Detection in `update_square`

Rewrote the movement logic. Now iterates over all squares and compares each one against every other (`if other is square: continue` — so it doesn’t compare itself to itself). If the square we’re comparing against (`other`) is bigger than the one being checked, we calculate the distance using the Pythagorean theorem (`math.hypot`). If that distance is less than `THREAT_RADIUS`, we record it as the closest threat in `closest_threat`.

After going through all squares, we have the nearest threat. Then we rotate the velocity vector to run directly away from it. We multiply by `max_speed` so it doesn’t run too slow or too fast — the closer the threat, the faster it reacts. The `* 0.1` factor makes the turn smooth instead of snappy like a teleport.

If there’s no threat nearby, jitter takes over — the square just drifts randomly like before.

## Passing `all_squares` to `update_square`

Updated the function call to pass 3 parameters:

```python
for square in squares:
    update_square(square, squares, dt_seconds)
```

Before it was just `square` and `dt_seconds`. Now `all_squares: list[Square]` is in the signature — that’s what we need for the loop above. Before this change, squares had no awareness of each other at all.

## FPS Counter

Added a font in `main()` for the FPS display:

```python
font = pygame.font.SysFont("Serif", 18)
```

You can change the font name and size, e.g. `("Arial", 24)`. If the font isn’t installed on the system, pygame falls back to its default — documented at https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont

Then rendered it in the corner as per the handout — white text, top-left:

```python
fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
screen.blit(fps_text, (10, 10))
```

## Initial Position in `update_square`

Lines 69–70 currently add velocity to position right at the start:

```python
x = float(square["x"]) + vx
y = float(square["y"]) + vy
```

This was needed earlier when there was no real movement logic. Now that speed and direction are driven by the threat system, you could change these to just:

```python
x = float(square["x"])
y = float(square["y"])
```

That makes movement slightly slower and possibly more natural. Worth trying both and picking whichever feels right.
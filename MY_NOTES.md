# i wanted explain everything that i have in read me here but i guess its became too professional

## Collision and Life Cycle Implementation:
To implement the "catch and kill" mechanic, I configured collision detection as a primary trigger. When a collision occurs, the target object is removed from the active list. Additionally, I implemented a spawn mechanism that adds and renders new squares over time to maintain the population.
## Chase Feature
Chase is the mirror of Flee:
Flee: smaller square steers AWAY from the nearest bigger one
Chase: bigger square steers TOWARD the nearest smaller one
Same vector logic, opposite direction.
Steering coefficient 0.08 (softer than flee 0.15).

## Wander
Applied at all times (not only in idle) by moving
apply_random_direction_jitter before the if/elif/else block.
This keeps randomness even during chase and flee
(I implemented this last time, so the code was just modified)
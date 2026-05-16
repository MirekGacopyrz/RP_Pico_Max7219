'''
The script implements a simple particle-system simulation on an 8×32 MAX7219 display.

Each particle:

has a position (x, y),
performs a random walk,
stores its own age counter.

During each iteration:

All particles move randomly by:
-1, 0, or +1 in the X direction,
-1, 0, or +1 in the Y direction.
After movement, collisions are checked:
if multiple particles occupy the same pixel,
all of them annihilate and are removed.
Every surviving particle increases its age.
After surviving 10 cycles:
a particle reproduces,
a new particle is spawned at distance 2 from the parent,
the parent age counter is reset.
The current state of the system is rendered on the display.

Additionally:

particles are constrained to the 32×8 display boundaries,
if the entire population disappears, a new random population is generated automatically.

The system behaves as a simplified model of:

diffusion,
annihilation reactions,
reproduction,
dynamic population equilibrium.
'''


from machine import Pin, SPI
import max7219
import time
import random

# =====================================
# MAX7219 INIT
# =====================================

spi = SPI(
    0,
    baudrate=10000000,
    polarity=1,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3)
)

cs = Pin(5, Pin.OUT)

display = max7219.Matrix8x8(spi, cs, 4)

display.brightness(2)

# =====================================
# DISPLAY SIZE
# =====================================

WIDTH = 32
HEIGHT = 8

# =====================================
# SETTINGS
# =====================================

NUM_PARTICLES = 10

BIRTH_AFTER = 10

# =====================================
# CREATE PARTICLES
# particle = [x, y, age]
# =====================================

particles = []

for i in range(NUM_PARTICLES):

    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)

    particles.append([x, y, 0])

# =====================================
# MAIN LOOP
# =====================================

while True:

    # =================================
    # MOVE PARTICLES
    # =================================

    moved_particles = []

    for particle in particles:

        x = particle[0]
        y = particle[1]
        age = particle[2]

        # losowy ruch

        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])

        x += dx
        y += dy

        # ograniczenie do ekranu

        if x < 0:
            x = 0

        if x >= WIDTH:
            x = WIDTH - 1

        if y < 0:
            y = 0

        if y >= HEIGHT:
            y = HEIGHT - 1

        moved_particles.append([x, y, age + 1])

    # =================================
    # ANNIHILATION
    # =================================

    counts = {}

    for p in moved_particles:

        pos = (p[0], p[1])

        if pos in counts:
            counts[pos] += 1
        else:
            counts[pos] = 1

    survivors = []

    for p in moved_particles:

        pos = (p[0], p[1])

        # przeżywają tylko samotne

        if counts[pos] == 1:
            survivors.append(p)

    particles = survivors

    # =================================
    # REPRODUCTION
    # =================================

    newborns = []

    for p in particles:

        x = p[0]
        y = p[1]
        age = p[2]

        # narodziny po 10 cyklach

        if age >= BIRTH_AFTER:

            # reset wieku rodzica

            p[2] = 0

            # nowe dziecko w odległości 2

            dx = random.choice([-2, 0, 2])
            dy = random.choice([-2, 0, 2])

            nx = x + dx
            ny = y + dy

            # ograniczenia ekranu

            if nx < 0:
                nx = 0

            if nx >= WIDTH:
                nx = WIDTH - 1

            if ny < 0:
                ny = 0

            if ny >= HEIGHT:
                ny = HEIGHT - 1

            newborns.append([nx, ny, 0])

    # dodanie nowych cząstek

    particles.extend(newborns)

    # =================================
    # DRAW
    # =================================

    display.fill(0)

    for p in particles:

        display.pixel(p[0], p[1], 1)

    display.show()

    # =================================
    # AUTO RESET IF EMPTY
    # =================================

    if len(particles) == 0:

        for i in range(NUM_PARTICLES):

            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)

            particles.append([x, y, 0])

    time.sleep(0.5)

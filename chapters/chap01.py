from tuples import *


class Projectile:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel


class Environment:
    def __init__(self, grav, wind):
        self.grav = grav
        self.wind = wind


def tick(env, proj):
    pos = proj.pos + proj.vel
    vel = proj.vel + env.grav + env.wind
    return Projectile(pos, vel)


def run():
    p = Projectile(Point(0, 1, 0), Vector(1, 1, 0).normalise())
    e = Environment(Vector(0, -0.1, 0), Vector(-0.08, 0, 0))
    count = 1
    while p.pos.y > 0:
        print(f'Tick {count}: Projectile position: {p.pos.x}, {p.pos.y}, {p.pos.z}')
        p = tick(e, p)
        count += 1


if __name__ == '__main__':
    run()

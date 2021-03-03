from tuples import *
from canvas import Canvas
from colours import Colour


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
    HEIGHT = 550
    p = Projectile(Point(0, 1, 0), Vector(1, 1.8, 0).normalise() * 11.25)
    e = Environment(Vector(0, -0.1, 0), Vector(-0.04, 0, 0))
    c = Canvas(400, HEIGHT)
    count = 1
    while p.pos.y > 0:
        c.write_pixel(int(p.pos.x), HEIGHT - int(p.pos.y), Colour(0.5, 0.2, 1))
        print(f'Tick {count}: Projectile position: {p.pos.x}, {p.pos.y}, {p.pos.z}')
        p = tick(e, p)
        count += 1
    c.write_to_ppm('..\\images\\projectile.ppm')


if __name__ == '__main__':
    run()

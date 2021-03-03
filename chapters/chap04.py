from matrices import Matrix
from tuples import Point
from canvas import Canvas
from colours import Colour
from math import pi


def run():
    # our clock face will be drawn in the x-y plane, so z-components will always be 0
    WIDTH = 500
    HEIGHT = 500
    c = Canvas(WIDTH, HEIGHT)
    for i in range(12):
        p = Point(0, 0, 0)
        # Move (translate) the point to the 12-o'clock position
        t = Matrix.translation(0, 200, 0)
        p12 = t * p
        # Rotate the point by -i * pi / 6 radians
        r = Matrix.rotation_z(-i * pi / 6)
#        pr = r * p12
#        c.write_pixel(int(pr.x + WIDTH / 2), int(HEIGHT / 2 - pr.y), Colour(0.5, 0.2, 1))

        # Create compound matrix (in reverse order!)
        trans_rot = r * t
        pr = trans_rot * p
        print_pixel_block(c, int(pr.x), int(pr.y))
    c.write_to_ppm('..\\images\\clock.ppm')


def print_pixel_block(c, x, y, size=5):
    for yy in range(y - size // 2, y + 1 + size // 2):
        for xx in range(x - size // 2, x + 1 + size // 2):
            c.write_pixel(int(xx + c.width / 2), int(c.height / 2 - yy), Colour(0.5, 0.2, 1))


if __name__ == '__main__':
    run()

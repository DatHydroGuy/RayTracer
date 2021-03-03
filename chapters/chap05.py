from matrices import Matrix
from rays import Ray
from canvas import Canvas
from primitives import Sphere
from colours import Colour
from tuples import *
from math import pi


def run():
    # Sphere will be located at (0, 0, 0)
    # We will be casting rays from (0, 0, -5)
    # Wall will be at z=10
    WIDTH = 100
    HEIGHT = 100
    c = Canvas(WIDTH, HEIGHT)
    s = Sphere()
    col = Colour(1, 0, 0)
    ray_origin = Point(0, 0, -5)
    wall_z = 10
    wall_width = 7
    wall_height = 7
    pixel_width = wall_width / WIDTH
    pixel_height = wall_height / HEIGHT
    half_width = wall_width / 2
    half_height = wall_height / 2

    # Transformations (optional)
    # s.transform = Matrix.scaling(1, 0.5, 1)
    # s.transform = Matrix.scaling(0.5, 1, 1)
    # s.transform = Matrix.rotation_z(pi / 4) * Matrix.scaling(0.5, 1, 1)
    # s.transform = Matrix.shearing(1, 0, 0, 0, 0, 0) * Matrix.scaling(0.5, 1, 1)

    for y in range(HEIGHT):
        world_y = half_height - pixel_height * y

        for x in range(WIDTH):
            world_x = -half_width + pixel_width * x

            point_on_wall = Point(world_x, world_y, wall_z)

            ray_direction = Vector.from_tuple(point_on_wall - ray_origin)
            r = Ray(ray_origin, ray_direction.normalise())
            xs = s.intersects(r)

            if len(xs) > 0:
                c.write_pixel(x, y, col)

    c.write_to_ppm('..\\images\\sphere_shadow.ppm')


if __name__ == '__main__':
    run()

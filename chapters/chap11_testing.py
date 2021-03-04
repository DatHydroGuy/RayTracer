from primitives import *
from world import World
from materials import Material
from lights import PointLight
from camera import Camera
from transformations import Transformations
from patterns import *
from math import pi


def run():
    world = World.default_world()

    ground = Plane()
    ground_pattern = StripePattern(Colour(1, 1, 0), Colour(0, 0, 1))
    ground_pattern.transform = Matrix.scaling(0.5, 0.5, 0.5)
    ground.material = Material()
    ground.material.colour = Colour(1, 0.9, 0.9)
    ground.material.specular = 0
    ground.material.reflective = 0.2
    ground.material.pattern = ground_pattern

    left_wall = Plane()
    left_wall_pattern = RingPattern(Colour(0, 1, 0), Colour(1, 0.5, 0))
    left_wall_pattern.transform = Matrix.scaling(0.5, 0.5, 0.5)
    left_wall.transform = Matrix.translation(0, 0, 5) * Matrix.rotation_y(-pi / 4) * Matrix.rotation_x(pi / 2)
    left_wall.material = Material()
    left_wall.material.colour = Colour(1, 0.9, 0.9)
    left_wall.material.specular = 0
    left_wall.material.reflective = 0.1
    left_wall.material.pattern = left_wall_pattern

    right_wall = Plane()
    right_wall_pattern = CheckersPattern(Colour(1, 0, 0), Colour(0, 1, 1))
    right_wall_pattern.transform = Matrix.scaling(0.75, 0.5, 0.5)
    right_wall.transform = Matrix.translation(0, 0, 5) * Matrix.rotation_y(pi / 4) * Matrix.rotation_x(pi / 2)
    right_wall.material = Material()
    right_wall.material.colour = Colour(1, 0.9, 0.9)
    right_wall.material.specular = 0
    right_wall.material.pattern = right_wall_pattern

    middle = Sphere()
    middle.transform = Matrix.translation(-0.5, 1, 0.5) * Matrix.rotation_x(-2 * pi / 3) * Matrix.rotation_z(pi / 3)
    middle.material = Material()
    middle.material.colour = Colour(0.1, 1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    middle.material.reflective = 0.1
    middle_sphere_pattern = GradientPattern(Colour(1, 0, 0), Colour(0, 0, 1))
    middle_sphere_pattern.transform = Matrix.translation(-1, 0, 0) * Matrix.scaling(2, 2, 2) * Matrix.rotation_z(pi / 3)
    middle.material.pattern = middle_sphere_pattern

    right = Sphere()
    right.transform = Matrix.translation(1.5, 0.5, -0.5) * Matrix.scaling(0.5, 0.5, 0.5) * \
        Matrix.rotation_x(2 * pi / 3) * Matrix.rotation_z(-pi / 4)
    right.material = Material()
    right.material.colour = Colour(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3
    right.material.reflective = 0.1
    right_sphere_pattern = StripePattern(Colour(1, 1, 0), Colour(0.4, 0, 1))
    right_sphere_pattern.transform = Matrix.scaling(0.1, 0.1, 0.1)
    right.material.pattern = right_sphere_pattern

    left = Sphere()
    left.transform = Matrix.translation(-1.5, 0.33, -0.75) * Matrix.scaling(0.33, 0.33, 0.33) * \
        Matrix.rotation_x(pi / 3) * Matrix.rotation_z(pi / 4)
    left.material = Material()
    left.material.colour = Colour(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3
    left_sphere_pattern = CheckersPattern(Colour(1, 0.8, 0.8), Colour(0.2, 0.2, 0.4))
    left_sphere_pattern.transform = Matrix.scaling(0.25, 0.5, 0.75)
    left.material.pattern = left_sphere_pattern

    world.lights[0] = PointLight(Point(-10, 10, -10), Colour(1, 1, 1))
    # world.lights.append(PointLight(Point(0, 10, -10), Colour(0.5, 0.5, 0.5)))
    # world.lights.append(PointLight(Point(10, 10, -10), Colour(0.5, 0, 0.5)))
    world.objects = [ground, left_wall, right_wall, middle, left, right]
    camera = Camera(1600, 900, pi / 3)
    camera.transform = Transformations.view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world, True)
    canvas.write_to_ppm('..\\images\\mirrored_spheres_and_planes.ppm')


if __name__ == '__main__':
    run()

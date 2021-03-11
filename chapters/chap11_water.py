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
    ground_pattern = CheckersPattern(WHITE, BLACK)
    ground_pattern.transform = Matrix.scaling(0.5, 0.5, 0.5)
    ground.material = Material()
    ground.material.colour = Colour(0.2, 0.2, 0.2)
    ground.material.specular = 0
    ground.material.pattern = ground_pattern

    water = Plane()
    water.transform = Matrix.translation(0, 1.5, 0)
    water.casts_shadow = False
    water.material = Material()
    water.material.colour = Colour(0.4, 0.4, 0.4)
    water.material.diffuse = 0.7
    water.material.specular = 1
    water.material.shininess = 100
    water.material.reflective = 0.6
    water.material.transparency = 0.9
    water.material.refractive_index = 1.333

    left_wall = Plane()
    left_wall.transform = Matrix.translation(0, 0, 5) * Matrix.rotation_y(-pi / 4) * Matrix.rotation_x(pi / 2)
    left_wall.material = Material()
    left_wall.material.pattern = ground_pattern

    right_wall = Plane()
    right_wall.transform = Matrix.translation(0, 0, 5) * Matrix.rotation_y(pi / 4) * Matrix.rotation_x(pi / 2)
    right_wall.material = Material()
    right_wall.material.pattern = ground_pattern

    middle = Sphere()
    middle.transform = Matrix.translation(-0.25, 0.75, 0.5) * Matrix.scaling(0.75, 0.75, 0.75)
    middle.material = Material()
    middle.material.colour = Colour(0, 0, 0.3)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    middle.material.reflective = 0.4
    middle.material.transparency = 0.9
    middle.material.refractive_index = 1.52

    right = Sphere()
    right.transform = Matrix.translation(1.5, 0.5, -0.5) * Matrix.scaling(0.5, 0.5, 0.5)
    right.material = Material()
    right.material.colour = Colour(0, 0, 0)
    right.material.diffuse = 0.7
    right.material.specular = 0.8
    right.material.reflective = 0.7
    right.material.transparency = 0.3
    right.material.refractive_index = 2.417

    left = Sphere()
    left.transform = Matrix.translation(-0.8, 0.8, -1) * Matrix.scaling(0.8, 0.8, 0.8)
    left.material = Material()
    left.material.colour = Colour(0.1, 0.1, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3
    left.material.reflective = 0.2
    left.material.transparency = 0.9
    left.material.refractive_index = 1.52

    world.lights[0] = PointLight(Point(-10, 10, -10), Colour(1, 1, 1))
    world.objects = [ground, water, left_wall, right_wall, middle, left, right]
    camera = Camera(800, 600, pi / 3)
    camera.transform = Transformations.view_transform(Point(0, 3, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world, 8, True)
    canvas.write_to_ppm('..\\images\\chapter11_water.ppm')


if __name__ == '__main__':
    run()

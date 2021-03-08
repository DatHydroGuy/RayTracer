from primitives import *
from world import World
from materials import Material
from lights import PointLight
from camera import Camera
from transformations import Transformations
from patterns import *
from math import pi


def run():
    world = World()

    ground = Plane()
    ground.transform = Matrix.translation(0, -5.1, 0)
    ground_pattern = CheckersPattern(BLACK, WHITE)
    ground_pattern.transform = Matrix.translation(0, 0.1, 0)
    ground.material = Material()
    ground.material.ambient = 0.9
    ground.material.pattern = ground_pattern

    glass = Sphere()
    glass.material = Material()
    glass.material.colour = Colour(0.5, 0.5, 0.5)
    glass.material.diffuse = 0.1
    glass.material.shininess = 300
    glass.material.reflective = 1
    glass.material.transparency = 1
    glass.material.refractive_index = 1.52

    middle = Sphere()
    middle.transform = Matrix.scaling(0.5, 0.5, 0.5)
    middle.material = Material()
    middle.material.colour = Colour(0.5, 0.5, 0.5)
    middle.material.diffuse = 0.1
    middle.material.shininess = 300
    middle.material.reflective = 1
    middle.material.transparency = 1
    middle.material.refractive_index = 1

    world.lights.append(PointLight(Point(20, 10, 0), Colour(1, 1, 1)))
    world.objects = [ground, glass, middle]
    camera = Camera(1000, 1000, pi / 3)
    camera.transform = Transformations.view_transform(Point(0, 2.5, 0), Point(0, 0, 0), Vector(1, 0, 0))
    canvas = camera.render(world, 5, True)
    canvas.write_to_ppm('..\\images\\glass_sphere_on_checker.ppm')


if __name__ == '__main__':
    run()

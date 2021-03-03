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
    ground.material = Material()
    ground.material.colour = Colour(0, 1, 0)
    ground.material.ambient = 0.5
    ground.material.specular = 0

    middle = Sphere()
    middle.transform = Matrix.translation(-0.5, 1, 0.5) * Matrix.rotation_x(-2 * pi / 3) * Matrix.rotation_z(pi / 3)
    middle.material = Material()
    middle.material.colour = Colour(1, 1, 1)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3

    world.lights[0] = PointLight(Point(-10, 10, -10), Colour(1, 0, 1))
    # world.lights.append(PointLight(Point(0, 10, -10), Colour(0.5, 0.5, 0.5)))
    world.objects = [ground, middle]
    camera = Camera(500, 250, pi / 3)
    camera.transform = Transformations.view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world)
    canvas.write_to_ppm('..\\images\\bug.ppm')


if __name__ == '__main__':
    run()

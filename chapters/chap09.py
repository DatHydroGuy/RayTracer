from primitives import *
from colours import Colour
from world import World
from materials import Material
from lights import PointLight
from matrices import Matrix
from camera import Camera
from transformations import Transformations
from math import pi


def run():
    world = World.default_world()

    floor = Plane()
    floor.material = Material()
    floor.material.colour = Colour(1, 0.9, 0.9)
    floor.material.specular = 0

    left_wall = Plane()
    left_wall.transform = Matrix.translation(0, 0, 5) * Matrix.rotation_y(-pi / 4) * Matrix.rotation_x(pi / 2)
    left_wall.material = floor.material

    right_wall = Plane()
    right_wall.transform = Matrix.translation(0, 0, 5) * Matrix.rotation_y(pi / 4) * Matrix.rotation_x(pi / 2)
    right_wall.material = floor.material

    middle = Sphere()
    middle.transform = Matrix.translation(-0.5, 1, 0.5)
    middle.material = Material()
    middle.material.colour = Colour(0.1, 1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3

    right = Sphere()
    right.transform = Matrix.translation(1.5, 0.5, -0.5) * Matrix.scaling(0.5, 0.5, 0.5)
    right.material = Material()
    right.material.colour = Colour(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3

    left = Sphere()
    left.transform = Matrix.translation(-1.5, 0.33, -0.75) * Matrix.scaling(0.33, 0.33, 0.33)
    left.material = Material()
    left.material.colour = Colour(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3

    world.lights[0] = PointLight(Point(-10, 10, -10), Colour(0.5, 0.5, 0))
    world.lights.append(PointLight(Point(0, 10, -10), Colour(0, 0.5, 0.5)))
    world.lights.append(PointLight(Point(10, 10, -10), Colour(0.5, 0, 0.5)))
    world.objects = [floor, left_wall, right_wall, middle, left, right]
    camera = Camera(500, 250, pi / 3)
    camera.transform = Transformations.view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world)
    canvas.write_to_ppm('..\\images\\spheres_and_plane.ppm')


if __name__ == '__main__':
    run()

from primitives import *
from world import World
from materials import Material
from lights import PointLight
from camera import Camera
from transformations import Transformations
from patterns import *
from math import pi


def run():
    # Chapter10 final image created with values scale=0.6, octaves=2, persistence=3, lacunarity=3
    scale = 0.6
    octaves = 2
    persistence = 3
    lacunarity = 3

    world = World.default_world()

    ground = Plane()
    ground.transform = Matrix.rotation_y(-pi * 0.15)
    base_pattern1 = StripePattern(WHITE, Colour(1, 0, 0))
    base_pattern2 = StripePattern(WHITE, Colour(1, 0, 0))
    base_pattern2.transform = Matrix.rotation_y(pi / 2)
    ground_pattern1 = PerturbedPattern(base_pattern1, scale, octaves, persistence, lacunarity)
    ground_pattern2 = PerturbedPattern(base_pattern2, scale, octaves, persistence, lacunarity)
    blended_pattern = BlendedPattern(ground_pattern1, ground_pattern2)
    ground.material = Material()
    ground.material.colour = Colour(1, 0, 0)
    ground.material.specular = 0
    ground.material.pattern = blended_pattern

    middle = Sphere()
    middle.transform = Matrix.translation(-0.5, 1, 0.5) * Matrix.rotation_y(-1.7) * \
        Matrix.rotation_x(-2.35) * Matrix.rotation_z(1.1)
    base_pattern3 = StripePattern(Colour(0, 0.8, 0.4), Colour(0.3, 1, 0.6))
    base_pattern3.transform = Matrix.scaling(1 / 3, 1 / 3, 1 / 3)
    sphere_pattern = PerturbedPattern(base_pattern3, scale, octaves, persistence, lacunarity)
    middle.material = Material()
    middle.material.colour = Colour(1, 1, 1)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    middle.material.pattern = sphere_pattern

    world.lights[0] = PointLight(Point(-10, 10, -10), Colour(1, 1, 1))
    # world.lights.append(PointLight(Point(0, 10, -10), Colour(0.5, 0.5, 0.5)))
    world.objects = [ground, middle]
    camera = Camera(800, 600, pi / 3)
    camera.transform = Transformations.view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world, True)
    canvas.write_to_ppm('..\\images\\pattern_test.ppm')


if __name__ == '__main__':
    run()

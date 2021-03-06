import unittest
from world import World
from lights import PointLight
from primitives import *
from matrices import Matrix
from tuples import *
from colours import Colour
from rays import Ray
from intersections import Intersection
from test_patterns import TestPattern


class WorldTestCase(unittest.TestCase):
    def test_creating_a_world(self):
        # Arrange
        w = World()

        # Act

        # Assert
        self.assertEqual(len(w.objects), 0)
        self.assertListEqual(w.lights, [])

    def test_the_default_world(self):
        # Arrange
        light = PointLight(Point(-10, 10, -10), Colour(1, 1, 1))
        s1 = Sphere()
        s1.material.colour = Colour(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular = 0.2
        s2 = Sphere()
        s2.transform = Matrix.scaling(0.5, 0.5, 0.5)

        # Act
        w = World.default_world()

        # Assert
        self.assertEqual(w.lights[0], light)
        self.assertTrue(s1 in w.objects)
        self.assertTrue(s2 in w.objects)

    def test_intersect_the_default_world_with_a_ray(self):
        # Arrange
        w = World.default_world()
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))

        # Act
        xs = w.intersect_world(ray)

        # Assert
        self.assertEqual(len(xs), 4)
        self.assertEqual(xs[0].t, 4)
        self.assertEqual(xs[1].t, 4.5)
        self.assertEqual(xs[2].t, 5.5)
        self.assertEqual(xs[3].t, 6)

    def test_shading_an_intersection_from_the_outside(self):
        # Arrange
        w = World.default_world()
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = w.objects[0]
        i = Intersection(4, shape)
        expected = Colour(0.38066, 0.47583, 0.2855)

        # Act
        comps = i.prepare_computations(ray)
        c = w.shade_hit(comps)

        # Assert
        self.assertEqual(c, expected)

    def test_shading_an_intersection_from_the_inside(self):
        # Arrange
        w = World.default_world()
        w.lights[0] = PointLight(Point(0, 0.25, 0), Colour(1, 1, 1))
        ray = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = w.objects[1]
        i = Intersection(0.5, shape)
        expected = Colour(0.90498, 0.90498, 0.90498)

        # Act
        comps = i.prepare_computations(ray)
        c = w.shade_hit(comps)

        # Assert
        self.assertEqual(c, expected)

    def test_the_colour_when_a_ray_misses(self):
        # Arrange
        w = World.default_world()
        ray = Ray(Point(0, 0, -5), Vector(0, 1, 0))
        expected = Colour(0, 0, 0)

        # Act
        c = w.colour_at(ray)

        # Assert
        self.assertEqual(c, expected)

    def test_the_colour_when_a_ray_hits(self):
        # Arrange
        w = World.default_world()
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        expected = Colour(0.38066, 0.47583, 0.2855)

        # Act
        c = w.colour_at(ray)

        # Assert
        self.assertEqual(c, expected)

    def test_the_colour_with_an_intersection_behind_the_ray(self):
        # Arrange
        w = World.default_world()
        outer = w.objects[0]
        outer.material.ambient = 1
        inner = w.objects[1]
        inner.material.ambient = 1
        ray = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))

        # Act
        c = w.colour_at(ray)

        # Assert
        self.assertEqual(c, inner.material.colour)

    def test_there_is_no_shadow_when_nothing_is_collinear_with_point_and_light(self):
        # Arrange
        w = World.default_world()
        point = Point(0, 10, 0)

        # Act
        result = w.is_shadowed(point)

        # Assert
        self.assertFalse(result)

    def test_there_is_a_shadow_when_an_object_lies_between_point_and_light(self):
        # Arrange
        w = World.default_world()
        point = Point(10, -10, 10)

        # Act
        result = w.is_shadowed(point)

        # Assert
        self.assertTrue(result)

    def test_there_is_no_shadow_when_object_is_behind_the_light(self):
        # Arrange
        w = World.default_world()
        point = Point(-20, 20, -20)

        # Act
        result = w.is_shadowed(point)

        # Assert
        self.assertFalse(result)

    def test_there_is_no_shadow_when_object_is_behind_the_point(self):
        # Arrange
        w = World.default_world()
        point = Point(-2, 2, -2)

        # Act
        result = w.is_shadowed(point)

        # Assert
        self.assertFalse(result)

    def test_when_shade_hit_is_given_an_intersection_in_shadow(self):
        # Arrange
        w = World()
        w.lights.append(PointLight(Point(0, 0, -10), Colour(1, 1, 1)))
        s1 = Sphere()
        w.objects.append(s1)
        s2 = Sphere()
        s2.transform = Matrix.translation(0, 0, 10)
        w.objects.append(s2)
        ray = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        intersect = Intersection(4, s2)
        expected = Colour(0.1, 0.1, 0.1)

        # Act
        comps = intersect.prepare_computations(ray)
        c = w.shade_hit(comps)

        # Assert
        self.assertEqual(c, expected)

    def test_the_reflected_colour_of_a_nonreflective_material_is_black(self):
        # Arrange
        w = World.default_world()
        ray = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = w.objects[1]
        shape.material.ambient = 1
        intersect = Intersection(1, shape)
        expected = Colour(0, 0, 0)

        # Act
        comps = intersect.prepare_computations(ray)
        c = w.reflected_colour(comps)

        # Assert
        self.assertEqual(c, expected)

    def test_the_reflected_colour_of_a_reflective_material(self):
        # Arrange
        w = World.default_world()
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transform = Matrix.translation(0, -1, 0)
        w.objects.append(shape)
        ray = Ray(Point(0, 0, -3), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        intersect = Intersection(sqrt(2), shape)
        expected = Colour(0.19033, 0.23792, 0.14275)

        # Act
        comps = intersect.prepare_computations(ray)
        c = w.reflected_colour(comps)

        # Assert
        self.assertEqual(c, expected)

    def test_shade_hit_with_a_reflective_material(self):
        # Arrange
        w = World.default_world()
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transform = Matrix.translation(0, -1, 0)
        w.objects.append(shape)
        ray = Ray(Point(0, 0, -3), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        intersect = Intersection(sqrt(2), shape)
        expected = Colour(0.87676, 0.92434, 0.82917)

        # Act
        comps = intersect.prepare_computations(ray)
        c = w.shade_hit(comps)

        # Assert
        self.assertEqual(c, expected)

    def test_colour_at_between_two_reflective_surfaces_should_terminate_successfully(self):
        # Arrange
        world = World()
        world.lights.append(PointLight(Point(0, 0, 0), Colour(1, 1, 1)))
        lower_plane = Plane()
        lower_plane.material = Material()
        lower_plane.material.reflective = 1
        lower_plane.transform = Matrix.translation(0, -1, 0)
        upper_plane = Plane()
        upper_plane.material = Material()
        upper_plane.material.reflective = 1
        upper_plane.transform = Matrix.translation(0, 1, 0)
        world.objects = [lower_plane, upper_plane]
        ray = Ray(Point(0, 0, 0), Vector(0, 1, 0))
        black = Colour(0, 0, 0)

        # Act
        colour = world.colour_at(ray)

        self.assertNotEqual(colour, black)

    def test_the_reflected_colour_at_the_maximum_recursive_depth(self):
        # Arrange
        world = World.default_world()
        shape = Plane()
        shape.material = Material()
        shape.material.reflective = 0.5
        shape.transform = Matrix.translation(0, -1, 0)
        world.objects = [shape]
        ray = Ray(Point(0, 0, -3), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        intersect = Intersection(sqrt(2), shape)
        expected = Colour(0, 0, 0)

        # Act
        comps = intersect.prepare_computations(ray)
        colour = world.reflected_colour(comps, 0)

        # Assert
        self.assertEqual(colour, expected)

    def test_the_refracted_colour_with_an_opaque_surface(self):
        # Arrange
        world = World.default_world()
        shape = world.objects[0]
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        intersects = Intersection.intersections(Intersection(4, shape), Intersection(6, shape))
        expected = Colour(0, 0, 0)

        # Act
        comps = intersects[0].prepare_computations(ray, intersects)
        colour = world.refracted_colour(comps, 5)

        # Assert
        self.assertEqual(colour, expected)

    def test_the_refracted_colour_at_the_maximum_recursive_depth(self):
        # Arrange
        world = World.default_world()
        shape = world.objects[0]
        shape.material.transparency = 1
        shape.material.refractive_index = 1.5
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        intersects = Intersection.intersections(Intersection(4, shape), Intersection(6, shape))
        expected = Colour(0, 0, 0)

        # Act
        comps = intersects[0].prepare_computations(ray, intersects)
        colour = world.refracted_colour(comps, 0)

        # Assert
        self.assertEqual(colour, expected)

    def test_the_refracted_colour_under_total_internal_reflection(self):
        # Arrange
        world = World.default_world()
        shape = world.objects[0]
        shape.material.transparency = 1
        shape.material.refractive_index = 1.5
        ray = Ray(Point(0, 0, sqrt(2) / 2), Vector(0, 1, 0))
        intersects = Intersection.intersections(Intersection(-sqrt(2) / 2, shape), Intersection(sqrt(2) / 2, shape))
        expected = Colour(0, 0, 0)

        # Act
        # Note: now the ray starts inside the sphere, so look at the SECOND intersection (intersects[1])
        comps = intersects[1].prepare_computations(ray, intersects)
        colour = world.refracted_colour(comps, 5)

        # Assert
        self.assertEqual(colour, expected)

    def test_the_refracted_colour_with_a_refracted_ray(self):
        # Arrange
        world = World.default_world()
        a = world.objects[0]
        a.material.ambient = 1
        a.material.pattern = TestPattern()
        b = world.objects[1]
        b.material.transparency = 1
        b.material.refractive_index = 1.5
        ray = Ray(Point(0, 0, 0.1), Vector(0, 1, 0))
        intersects = Intersection.intersections(Intersection(-0.9899, a), Intersection(-0.4899, b),
                                                Intersection(0.4899, b), Intersection(0.9899, a))
        expected = Colour(0, 0.99887, 0.04722)

        # Act
        comps = intersects[2].prepare_computations(ray, intersects)
        colour = world.refracted_colour(comps, 5)

        # Assert
        self.assertEqual(colour, expected)

    def test_shade_hit_with_a_transparent_material(self):
        # Arrange
        w = World.default_world()
        ground = Plane()
        ground.transform = Matrix.translation(0, -1, 0)
        ground.material.transparency = 0.5
        ground.material.refractive_index = 1.5
        w.objects.append(ground)
        ball = Sphere()
        ball.transform = Matrix.translation(0, -3.5, -0.5)
        ball.material.colour = Colour(1, 0, 0)
        ball.material.ambient = 0.5
        w.objects.append(ball)
        ray = Ray(Point(0, 0, -3), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        intersects = Intersection.intersections(Intersection(sqrt(2), ground))
        expected = Colour(0.93642, 0.68642, 0.68642)

        # Act
        comps = intersects[0].prepare_computations(ray, intersects)
        colour = w.shade_hit(comps, 5)

        # Assert
        self.assertEqual(colour, expected)

    def test_shade_hit_with_a_reflective_and_transparent_material(self):
        # Arrange
        rtot = sqrt(2) / 2
        w = World.default_world()
        ground = Plane()
        ground.transform = Matrix.translation(0, -1, 0)
        ground.material.reflective = 0.5
        ground.material.transparency = 0.5
        ground.material.refractive_index = 1.5
        w.objects.append(ground)
        ball = Sphere()
        ball.transform = Matrix.translation(0, -3.5, -0.5)
        ball.material.colour = Colour(1, 0, 0)
        ball.material.ambient = 0.5
        w.objects.append(ball)
        ray = Ray(Point(0, 0, -3), Vector(0, -rtot, rtot))
        intersects = Intersection.intersections(Intersection(sqrt(2), ground))
        expected = Colour(0.93391, 0.69643, 0.69243)

        # Act
        comps = intersects[0].prepare_computations(ray, intersects)
        colour = w.shade_hit(comps, 5)

        # Assert
        self.assertEqual(colour, expected)


if __name__ == '__main__':
    unittest.main()

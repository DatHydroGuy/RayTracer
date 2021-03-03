import unittest
from world import World
from lights import PointLight
from primitives import Sphere
from matrices import Matrix
from tuples import *
from colours import Colour
from rays import Ray
from intersections import Intersection


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


if __name__ == '__main__':
    unittest.main()

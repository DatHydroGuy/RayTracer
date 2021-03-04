import unittest
from primitives import *
from rays import Ray
from tuples import *
from matrices import Matrix


class IntersectionsTestCase(unittest.TestCase):
    def test_intersection_encapsulates_t_and_an_object(self):
        # Arrange
        s = Sphere()

        # Act
        i = Intersection(3.5, s)

        # Assert
        self.assertEqual(i.t, 3.5)
        self.assertEqual(i.object, s)

    def test_aggregating_intersections(self):
        # Arrange
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)

        # Act
        xs = Intersection.intersections(i1, i2)

        # Assert
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[1].t, 2)

    def test_the_hit_when_all_intersections_have_positive_t_values(self):
        # Arrange
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersection.intersections(i1, i2)

        # Act
        i = Intersection.hit(xs)

        # Assert
        self.assertEqual(i, i1)

    def test_the_hit_when_some_intersections_have_negative_t_values(self):
        # Arrange
        s = Sphere()
        i1 = Intersection(-1, s)
        i2 = Intersection(1, s)
        xs = Intersection.intersections(i1, i2)

        # Act
        i = Intersection.hit(xs)

        # Assert
        self.assertEqual(i, i2)

    def test_the_hit_when_all_intersections_have_negative_t_values(self):
        # Arrange
        s = Sphere()
        i1 = Intersection(-1, s)
        i2 = Intersection(-2, s)
        xs = Intersection.intersections(i1, i2)

        # Act
        i = Intersection.hit(xs)

        # Assert
        self.assertIsNone(i)

    def test_the_hit_is_the_lowest_non_negative_t_value(self):
        # Arrange
        s = Sphere()
        i1 = Intersection(5, s)
        i2 = Intersection(2, s)
        i3 = Intersection(-3, s)
        i4 = Intersection(7, s)
        xs = Intersection.intersections(i1, i2, i3, i4)

        # Act
        i = Intersection.hit(xs)

        # Assert
        self.assertEqual(i, i2)

    def test_precomputing_the_state_of_an_intersection(self):
        # Arrange
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        expected_point = Point(0, 0, -1)
        expected_eye_vector = Vector(0, 0, -1)
        expected_normal_vector = Vector(0, 0, -1)

        # Act
        comps = i.prepare_computations(r)

        # Assert
        self.assertEqual(comps.t, i.t)
        self.assertEqual(comps.object, i.object)
        self.assertEqual(comps.point, expected_point)
        self.assertEqual(comps.eye_vector, expected_eye_vector)
        self.assertEqual(comps.normal_vector, expected_normal_vector)

    def test_precomputing_the_hit_when_intersection_occurs_on_the_outside(self):
        # Arrange
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)

        # Act
        comps = i.prepare_computations(r)

        # Assert
        self.assertFalse(comps.inside)

    def test_precomputing_the_hit_when_intersection_occurs_on_the_inside(self):
        # Arrange
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(1, shape)
        expected_point = Point(0, 0, 1)
        expected_eye_vector = Vector(0, 0, -1)
        expected_normal_vector = Vector(0, 0, -1)

        # Act
        comps = i.prepare_computations(r)

        # Assert
        self.assertEqual(comps.t, i.t)
        self.assertEqual(comps.object, i.object)
        self.assertEqual(comps.point, expected_point)
        self.assertEqual(comps.eye_vector, expected_eye_vector)
        self.assertEqual(comps.normal_vector, expected_normal_vector)
        self.assertTrue(comps.inside)

    def test_the_hit_should_offset_the_point(self):
        # Arrange
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        shape.transform = Matrix.translation(0, 0, 1)
        i = Intersection(5, shape)

        # Act
        comps = i.prepare_computations(r)

        # Assert
        self.assertLess(comps.over_point.z, -i.EPSILON / 2)
        self.assertGreater(comps.point.z, comps.over_point.z)

    def test_the_reflection_vector_is_precomputed(self):
        # Arrange
        shape = Plane()
        r = Ray(Point(0, 1, -1), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        i = Intersection(sqrt(2), shape)

        # Act
        comps = i.prepare_computations(r)

        # Assert
        self.assertEqual(comps.reflect_vector, Vector(0, sqrt(2) / 2, sqrt(2) / 2))


if __name__ == '__main__':
    unittest.main()

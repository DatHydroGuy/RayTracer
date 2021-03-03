import unittest
from tuples import Point, Vector
from matrices import Matrix
from rays import Ray


class RaysTestCase(unittest.TestCase):
    def test_creating_and_querying_a_ray(self):
        # Arrange
        origin = Point(1, 2, 3)
        direction = Vector(4, 5, 6)

        # Act
        r = Ray(origin, direction)

        # Assert
        self.assertEqual(r.origin, origin)
        self.assertEqual(r.direction, direction)

    def test_computing_a_point_from_a_distance(self):
        # Arrange
        r = Ray(Point(2, 3, 4), Vector(1, 0, 0))
        e1 = Point(2, 3, 4)
        e2 = Point(3, 3, 4)
        e3 = Point(1, 3, 4)
        e4 = Point(4.5, 3, 4)

        # Act
        r1 = r.position(0)
        r2 = r.position(1)
        r3 = r.position(-1)
        r4 = r.position(2.5)

        # Assert
        self.assertEqual(r1, e1)
        self.assertEqual(r2, e2)
        self.assertEqual(r3, e3)
        self.assertEqual(r4, e4)

    def test_translating_a_ray(self):
        # Arrange
        r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
        m = Matrix.translation(3, 4, 5)
        exp_origin = Point(4, 6, 8)
        exp_direction = Vector(0, 1, 0)

        # Act
        r2 = r.transform(m)

        # Assert
        self.assertEqual(r2.origin, exp_origin)
        self.assertEqual(r2.direction, exp_direction)

    def test_scaling_a_ray(self):
        # Arrange
        r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
        m = Matrix.scaling(2, 3, 4)
        exp_origin = Point(2, 6, 12)
        exp_direction = Vector(0, 3, 0)

        # Act
        r2 = r.transform(m)

        # Assert
        self.assertEqual(r2.origin, exp_origin)
        self.assertEqual(r2.direction, exp_direction)


if __name__ == '__main__':
    unittest.main()

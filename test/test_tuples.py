import unittest
from tuples import *
from math import sqrt


class VectorTestCase(unittest.TestCase):
    def test_tuple_with_w_value_of_1_is_a_point(self):
        # Arrange

        # Act
        a = Tuple(4.3, -4.2, 3.1, 1.0)

        # Assert
        self.assertEqual(a.x, 4.3)
        self.assertEqual(a.y, -4.2)
        self.assertEqual(a.z, 3.1)
        self.assertEqual(a.w, 1.0)
        self.assertTrue(a.is_point)
        self.assertFalse(a.is_vector)

    def test_tuple_with_w_value_of_0_is_a_vector(self):
        # Arrange

        # Act
        a = Tuple(4.3, -4.2, 3.1, 0.0)

        # Assert
        self.assertEqual(a.x, 4.3)
        self.assertEqual(a.y, -4.2)
        self.assertEqual(a.z, 3.1)
        self.assertEqual(a.w, 0.0)
        self.assertFalse(a.is_point)
        self.assertTrue(a.is_vector)

    def test_point_creates_tuple_with_w_value_of_1(self):
        # Arrange
        expected = Tuple(4, -4, 3, 1)

        # Act
        a = Point(4, -4, 3)

        # Assert
        self.assertEqual(a, expected)

    def test_vector_creates_tuple_with_w_value_of_0(self):
        # Arrange
        expected = Tuple(4, -4, 3, 0)

        # Act
        a = Vector(4, -4, 3)

        # Assert
        self.assertEqual(a, expected)

    def test_adding_two_tuples_together_creates_a_tuple(self):
        # Arrange
        expected = Tuple(1, 1, 6, 1)

        # Act
        a1 = Tuple(3, -2, 5, 1)
        a2 = Tuple(-2, 3, 1, 0)

        # Assert
        self.assertEqual(a1 + a2, expected)

    def test_subtracting_two_points_creates_a_vector(self):
        # Arrange
        expected = Vector(-2, -4, -6)

        # Act
        a1 = Point(3, 2, 1)
        a2 = Point(5, 6, 7)

        # Assert
        self.assertEqual(a1 - a2, expected)

    def test_subtracting_a_vector_from_a_point_creates_a_point(self):
        # Arrange
        expected = Point(-2, -4, -6)

        # Act
        a1 = Point(3, 2, 1)
        a2 = Vector(5, 6, 7)

        # Assert
        self.assertEqual(a1 - a2, expected)

    def test_subtracting_two_vectors_creates_another_vector(self):
        # Arrange
        expected = Vector(-2, -4, -6)

        # Act
        a1 = Vector(3, 2, 1)
        a2 = Vector(5, 6, 7)

        # Assert
        self.assertEqual(a1 - a2, expected)

    def test_subtracting_a_vector_from_the_zero_vector(self):
        # Arrange
        expected = Vector(-1, 2, -3)

        # Act
        zero = Vector(0, 0, 0)
        a1 = Vector(1, -2, 3)

        # Assert
        self.assertEqual(zero - a1, expected)

    def test_negating_a_tuple_creates_a_componentwise_negative_tuple(self):
        # Arrange
        expected = Tuple(-1, 2, -3, 4)

        # Act
        a = Tuple(1, -2, 3, -4)

        # Assert
        self.assertEqual(-a, expected)

    def test_multiplying_a_tuple_by_a_scalar(self):
        # Arrange
        expected = Tuple(3.5, -7, 10.5, -14)

        # Act
        a = Tuple(1, -2, 3, -4)

        # Assert
        self.assertEqual(a * 3.5, expected)

    def test_multiplying_a_tuple_by_a_fraction(self):
        # Arrange
        expected = Tuple(0.5, -1, 1.5, -2)

        # Act
        a = Tuple(1, -2, 3, -4)

        # Assert
        self.assertEqual(a * 0.5, expected)

    def test_dividing_a_tuple_by_a_scalar(self):
        # Arrange
        expected = Tuple(0.5, -1, 1.5, -2)

        # Act
        a = Tuple(1, -2, 3, -4)

        # Assert
        self.assertEqual(a / 2, expected)

    def test_magnitude_of_x_vector(self):
        # Arrange
        expected = 1

        # Act
        a = Vector(1, 0, 0)

        # Assert
        self.assertEqual(a.mag, expected)

    def test_magnitude_of_y_vector(self):
        # Arrange
        expected = 1

        # Act
        a = Vector(0, 1, 0)

        # Assert
        self.assertEqual(a.mag, expected)

    def test_magnitude_of_z_vector(self):
        # Arrange
        expected = 1

        # Act
        a = Vector(0, 0, 1)

        # Assert
        self.assertEqual(a.mag, expected)

    def test_magnitude_of_positive_vector(self):
        # Arrange
        expected = sqrt(14)

        # Act
        a = Vector(1, 2, 3)

        # Assert
        self.assertEqual(a.mag, expected)

    def test_magnitude_of_negative_vector(self):
        # Arrange
        expected = sqrt(14)

        # Act
        a = Vector(-1, -2, -3)

        # Assert
        self.assertEqual(a.mag, expected)

    def test_normalising_an_axial_vector(self):
        # Arrange
        expected = Vector(1, 0, 0)

        # Act
        a = Vector(4, 0, 0)

        # Assert
        self.assertEqual(a.normalise(), expected)

    def test_normalising_a_vector(self):
        # Arrange
        expected = Vector(1 / sqrt(14), 2 / sqrt(14), 3 / sqrt(14))

        # Act
        a = Vector(1, 2, 3)

        # Assert
        self.assertEqual(a.normalise(), expected)

    def test_magnitude_of_a_normalised_vector_is_1(self):
        # Arrange
        expected = 1

        # Act
        a = Vector(1, 2, 3)

        # Assert
        self.assertEqual(a.normalise().mag, expected)

    def test_dot_product_of_two_vectors(self):
        # Arrange
        expected = 20

        # Act
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 4)

        # Assert
        self.assertEqual(a.dot(b), expected)

    def test_dot_product_of_two_tuples(self):
        # Arrange
        expected = 4

        # Act
        a = Tuple(1, 2, 3, 4)
        b = Tuple(2, 3, 4, -4)

        # Assert
        self.assertEqual(a.dot(b), expected)

    def test_cross_product_of_two_vectors(self):
        # Arrange
        expected1 = Vector(-1, 2, -1)
        expected2 = Vector(1, -2, 1)

        # Act
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 4)

        # Assert
        self.assertEqual(a.cross(b), expected1)
        self.assertEqual(b.cross(a), expected2)

    def test_multiplying_a_vector_by_a_scalar(self):
        # Arrange
        a = Vector(1, 2, 3)
        expected = Vector(2.5, 5, 7.5)

        # Act
        result = a * 2.5

        # Assert
        self.assertEqual(result, expected)

    def test_multiplying_a_scalar_by_a_vector(self):
        # Arrange
        a = Vector(1, 2, 3)
        expected = Vector(2.5, 5, 7.5)

        # Act
        result = 2.5 * a

        # Assert
        self.assertEqual(result, expected)

    def test_create_a_point_from_a_tuple(self):
        # Arrange
        a = Point(1, 2, 3)
        b = Point(2, 5, 8)
        expected = Point(1, 3, 5)

        # Act
        result = Point.from_tuple(b - a)

        # Assert
        self.assertEqual(result, expected)

    def test_create_a_Vector_from_a_tuple(self):
        # Arrange
        a = Point(1, 2, 3)
        b = Point(2, 5, 8)
        expected = Vector(1, 3, 5)

        # Act
        result = Vector.from_tuple(b - a)

        # Assert
        self.assertEqual(result, expected)

    def test_reflecting_a_Vector_approaching_at_45_degrees(self):
        # Arrange
        v = Vector(1, -1, 0)
        n = Vector(0, 1, 0)
        expected = Vector(1, 1, 0)

        # Act
        result = v.reflect(n)

        # Assert
        self.assertEqual(result, expected)

    def test_reflecting_a_Vector_off_a_slanted_surface(self):
        # Arrange
        v = Vector(0, -1, 0)
        n = Vector(sqrt(2) / 2, sqrt(2) / 2, 0)
        expected = Vector(1, 0, 0)

        # Act
        result = v.reflect(n)

        # Assert
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

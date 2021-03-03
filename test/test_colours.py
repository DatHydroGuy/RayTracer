import unittest
from colours import *


class ColourTestCase(unittest.TestCase):
    def test_colours_are_red_green_blue_tuples(self):
        # Arrange

        # Act
        c = Colour(-0.5, 0.4, 1.7)

        # Assert
        self.assertEqual(c.red, -0.5)
        self.assertEqual(c.green, 0.4)
        self.assertEqual(c.blue, 1.7)

    def test_adding_colours(self):
        # Arrange
        c1 = Colour(0.9, 0.6, 0.75)
        c2 = Colour(0.7, 0.1, 0.25)
        expected = Colour(1.6, 0.7, 1.0)

        # Act
        c3 = c1 + c2

        # Assert
        self.assertEqual(c3, expected)

    def test_subtracting_colours(self):
        # Arrange
        c1 = Colour(0.9, 0.6, 0.75)
        c2 = Colour(0.7, 0.1, 0.25)
        expected = Colour(0.2, 0.5, 0.5)

        # Act
        c3 = c1 - c2

        # Assert
        self.assertEqual(c3, expected)

    def test_multiplying_colour_by_a_scalar(self):
        # Arrange
        c = Colour(0.2, 0.3, 0.4)
        expected = Colour(0.4, 0.6, 0.8)

        # Act
        c2 = c * 2

        # Assert
        self.assertEqual(c2, expected)

    def test_multiplying_colours(self):
        # Arrange
        c1 = Colour(1, 0.2, 0.4)
        c2 = Colour(0.9, 1, 0.1)
        expected = Colour(0.9, 0.2, 0.04)

        # Act
        c3 = c1 * c2

        # Assert
        self.assertEqual(c3, expected)


if __name__ == '__main__':
    unittest.main()

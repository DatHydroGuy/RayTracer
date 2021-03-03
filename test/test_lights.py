import unittest
from lights import PointLight
from tuples import *
from colours import Colour


class LightsTestCase(unittest.TestCase):
    def test_a_point_light_has_a_position_and_intensity(self):
        # Arrange
        intensity = Colour(1, 1, 1)
        position = Point(0, 0, 0)

        # Act
        light = PointLight(position, intensity)

        # Assert
        self.assertEqual(light.position, position)
        self.assertEqual(light.intensity, intensity)


if __name__ == '__main__':
    unittest.main()

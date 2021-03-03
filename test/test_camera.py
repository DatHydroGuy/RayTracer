import sys
sys.path.append('..')
import unittest
from math import pi, sqrt
from camera import Camera
from matrices import Matrix
from tuples import *
from transformations import Transformations
from colours import Colour
from world import World


class CameraTestCase(unittest.TestCase):
    def test_constructing_a_camera(self):
        # Arrange
        h_size = 160
        v_size = 120
        field_of_view = pi / 2

        # Act
        c = Camera(h_size, v_size, field_of_view)

        # Assert
        self.assertEqual(c.hsize, h_size)
        self.assertEqual(c.vsize, v_size)
        self.assertEqual(c.field_of_view, field_of_view)
        self.assertEqual(c.transform, Matrix.identity(4))

    def test_the_camera_pixel_size_for_a_horizontal_canvas(self):
        # Arrange
        h_size = 200
        v_size = 125
        field_of_view = pi / 2

        # Act
        c = Camera(h_size, v_size, field_of_view)

        # Assert
        self.assertAlmostEqual(c.pixel_size, 0.01)

    def test_the_camera_pixel_size_for_a_vertical_canvas(self):
        # Arrange
        h_size = 125
        v_size = 200
        field_of_view = pi / 2

        # Act
        c = Camera(h_size, v_size, field_of_view)

        # Assert
        self.assertAlmostEqual(c.pixel_size, 0.01)

    def test_constructing_a_ray_through_the_center_of_the_canvas(self):
        # Arrange
        h_size = 201
        v_size = 101
        field_of_view = pi / 2
        c = Camera(h_size, v_size, field_of_view)
        expected_origin = Point(0, 0, 0)
        expected_direction = Vector(0, 0, -1)

        # Act
        r = c.ray_for_pixel(100, 50)

        # Assert
        self.assertEqual(r.origin, expected_origin)
        self.assertEqual(r.direction, expected_direction)

    def test_constructing_a_ray_through_the_corner_of_the_canvas(self):
        # Arrange
        h_size = 201
        v_size = 101
        field_of_view = pi / 2
        c = Camera(h_size, v_size, field_of_view)
        expected_origin = Point(0, 0, 0)
        expected_direction = Vector(0.66519, 0.33259, -0.66851)

        # Act
        r = c.ray_for_pixel(0, 0)

        # Assert
        self.assertEqual(r.origin, expected_origin)
        self.assertEqual(r.direction, expected_direction)

    def test_constructing_a_ray_when_the_camera_is_transformed(self):
        # Arrange
        h_size = 201
        v_size = 101
        field_of_view = pi / 2
        c = Camera(h_size, v_size, field_of_view)
        c.transform = Matrix.rotation_y(pi / 4) * Matrix.translation(0, -2, 5)
        expected_origin = Point(0, 2, -5)
        expected_direction = Vector(sqrt(2) / 2, 0, -sqrt(2) / 2)

        # Act
        r = c.ray_for_pixel(100, 50)

        # Assert
        self.assertEqual(r.origin, expected_origin)
        self.assertEqual(r.direction, expected_direction)

    def test_rendering_a_world_with_a_camera(self):
        # Arrange
        w = World.default_world()
        h_size = 11
        v_size = 11
        field_of_view = pi / 2
        c = Camera(h_size, v_size, field_of_view)
        from_pt = Point(0, 0, -5)
        to_pt = Point(0, 0, 0)
        up_vec = Vector(0, 1, 0)
        c.transform = Transformations.view_transform(from_pt, to_pt, up_vec)
        # expected = Colour(0.38066, 0.47583, 0.2855)
        expected = Colour(0.38039, 0.47451, 0.28627)

        # Act
        image = c.render(w)

        # Assert
        self.assertEqual(image.get_pixel(5, 5), expected)


if __name__ == '__main__':
    unittest.main()

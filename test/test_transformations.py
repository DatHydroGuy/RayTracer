import unittest
from transformations import Transformations
from tuples import *
from matrices import Matrix


class TransformationsTestCase(unittest.TestCase):
    def test_the_transformation_matrix_for_the_default_orientation(self):
        # Arrange
        from_pt = Point(0, 0, 0)
        to_pt = Point(0, 0, -1)
        up = Vector(0, 1, 0)

        # Act
        t = Transformations.view_transform(from_pt, to_pt, up)

        # Assert
        self.assertEqual(t, Matrix.identity(4))

    def test_the_transformation_matrix_looking_in_the_positive_z_direction(self):
        # Arrange
        from_pt = Point(0, 0, 0)
        to_pt = Point(0, 0, 1)
        up = Vector(0, 1, 0)

        # Act
        t = Transformations.view_transform(from_pt, to_pt, up)

        # Assert
        self.assertEqual(t, Matrix.scaling(-1, 1, -1))

    def test_the_view_transformation_moves_the_world_and_not_the_camera(self):
        # Arrange
        from_pt = Point(0, 0, 8)
        to_pt = Point(0, 0, 0)
        up = Vector(0, 1, 0)

        # Act
        t = Transformations.view_transform(from_pt, to_pt, up)

        # Assert
        self.assertEqual(t, Matrix.translation(0, 0, -8))

    def test_an_arbitrary_view_transformation(self):
        # Arrange
        from_pt = Point(1, 3, 2)
        to_pt = Point(4, -2, 8)
        up = Vector(1, 1, 0)
        expected = Matrix([[-0.50709, 0.50709, 0.67612, -2.36643], [0.76772, 0.60609, 0.12122, -2.82843],
                           [-0.35857, 0.59761, -0.71714, 0.00000], [0.00000, 0.00000, 0.00000, 1.00000]])

        # Act
        t = Transformations.view_transform(from_pt, to_pt, up)

        # Assert
        self.assertEqual(t, expected)


if __name__ == '__main__':
    unittest.main()

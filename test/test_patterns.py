import unittest
from patterns import *
from colours import Colour
from primitives import *
from math import pi


class TestPattern(Pattern):
    def __init__(self, colour_a=WHITE, colour_b=BLACK):
        super().__init__(colour_a, colour_b)

    def pattern_at(self, point):
        return Colour(point.x, point.y, point.z)

    def pattern_at_shape(self, shape, point):
        return super(TestPattern, self).pattern_at_shape(shape, point)


class PatternsTestCase(unittest.TestCase):
    def test_black_exists(self):
        # Arrange
        expected = Colour(0, 0, 0)

        # Act
        black = BLACK

        # Assert
        self.assertEqual(black, expected)

    def test_white_exists(self):
        # Arrange
        expected = Colour(1, 1, 1)

        # Act
        black = WHITE

        # Assert
        self.assertEqual(black, expected)

    def test_default_pattern_transformation(self):
        # Arrange
        expected = Matrix.identity(4)

        # Act
        c = TestPattern()

        # Assert
        self.assertEqual(c.transform, expected)

    def test_assigning_a_pattern_transformation(self):
        # Arrange
        c = TestPattern()
        expected = Matrix.translation(1, 2, 3)

        # Act
        c.transform = Matrix.translation(1, 2, 3)

        # Assert
        self.assertEqual(c.transform, expected)

    def test_a_pattern_with_an_object_transformation(self):
        # Arrange
        s = Sphere()
        s.transform = Matrix.scaling(2, 2, 2)
        p = TestPattern()
        expected = Colour(1, 1.5, 2)

        # Act
        c = p.pattern_at_shape(s, Point(2, 3, 4))

        # Assert
        self.assertEqual(c, expected)

    def test_a_pattern_with_a_pattern_transformation(self):
        # Arrange
        s = Sphere()
        p = TestPattern()
        p.transform = Matrix.scaling(2, 2, 2)
        expected = Colour(1, 1.5, 2)

        # Act
        c = p.pattern_at_shape(s, Point(2, 3, 4))

        # Assert
        self.assertEqual(c, expected)

    def test_a_pattern_with_an_object_and_a_pattern_transformation(self):
        # Arrange
        s = Sphere()
        s.transform = Matrix.scaling(2, 2, 2)
        p = TestPattern()
        p.transform = Matrix.translation(0.5, 1, 1.5)
        expected = Colour(0.75, 0.5, 0.25)

        # Act
        c = p.pattern_at_shape(s, Point(2.5, 3, 3.5))

        # Assert
        self.assertEqual(c, expected)


class StripedPatternTestCase(unittest.TestCase):
    def test_create_a_striped_pattern(self):
        # Arrange

        # Act
        pattern = StripePattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.a, WHITE)
        self.assertEqual(pattern.b, BLACK)

    def test_a_striped_pattern_is_constant_in_y(self):
        # Arrange

        # Act
        pattern = StripePattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 1, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 2, 0)), WHITE)

    def test_a_striped_pattern_is_constant_in_z(self):
        # Arrange

        # Act
        pattern = StripePattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 1)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 2)), WHITE)

    def test_a_striped_pattern_alternates_in_x(self):
        # Arrange

        # Act
        pattern = StripePattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0.9, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(1, 0, 0)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(-0.1, 0, 0)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(-1, 0, 0)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(-1.1, 0, 0)), WHITE)

    def test_stripes_with_an_object_transformation(self):
        # Arrange
        s = Sphere()
        s.set_transform(Matrix.scaling(2, 2, 2))
        pattern = StripePattern(WHITE, BLACK)

        # Act
        c = pattern.pattern_at_shape(s, Point(1.5, 0, 0))

        # Assert
        self.assertEqual(c, WHITE)

    def test_stripes_with_a_pattern_transformation(self):
        # Arrange
        s = Sphere()
        pattern = StripePattern(WHITE, BLACK)
        pattern.transform = Matrix.scaling(2, 2, 2)

        # Act
        c = pattern.pattern_at_shape(s, Point(1.5, 0, 0))

        # Assert
        self.assertEqual(c, WHITE)

    def test_stripes_with_both_an_object_and_a_pattern_transformation(self):
        # Arrange
        s = Sphere()
        s.set_transform(Matrix.scaling(2, 2, 2))
        pattern = StripePattern(WHITE, BLACK)
        pattern.transform = Matrix.translation(0.5, 0, 0)

        # Act
        c = pattern.pattern_at_shape(s, Point(2.5, 0, 0))

        # Assert
        self.assertEqual(c, WHITE)


class GradientPatternTestCase(unittest.TestCase):
    def test_a_gradient_linearly_interpolates_between_colours(self):
        # Arrange

        # Act
        pattern = GradientPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0.25, 0, 0)), Colour(0.75, 0.75, 0.75))
        self.assertEqual(pattern.pattern_at(Point(0.5, 0, 0)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(0.75, 0, 0)), Colour(0.25, 0.25, 0.25))
        self.assertEqual(pattern.pattern_at(Point(1, 0, 0)), BLACK)


class DoubleGradientPatternTestCase(unittest.TestCase):
    def test_a_double_gradient_linearly_interpolates_between_colours_in_first_half(self):
        # Arrange

        # Act
        pattern = DoubleGradientPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0.125, 0, 0)), Colour(0.75, 0.75, 0.75))
        self.assertEqual(pattern.pattern_at(Point(0.25, 0, 0)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(0.375, 0, 0)), Colour(0.25, 0.25, 0.25))
        self.assertEqual(pattern.pattern_at(Point(0.5, 0, 0)), BLACK)

    def test_a_double_gradient_reverse_linearly_interpolates_between_colours_in_second_half(self):
        # Arrange

        # Act
        pattern = DoubleGradientPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(1, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0.875, 0, 0)), Colour(0.75, 0.75, 0.75))
        self.assertEqual(pattern.pattern_at(Point(0.75, 0, 0)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(0.625, 0, 0)), Colour(0.25, 0.25, 0.25))
        self.assertEqual(pattern.pattern_at(Point(0.5, 0, 0)), BLACK)


class RingPatternTestCase(unittest.TestCase):
    def test_a_ring_pattern_should_extend_in_both_x_and_z(self):
        # Arrange

        # Act
        pattern = RingPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(1, 0, 0)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 1)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(0.708, 0, 0.708)), BLACK)


class GradientRingPatternTestCase(unittest.TestCase):
    def test_a_gradient_ring_linearly_interpolates_in_both_x_and_z_directions(self):
        # Arrange

        # Act
        pattern = GradientRingPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0.25, 0, 0)), Colour(0.75, 0.75, 0.75))
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0.5)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(0, 0, -0.75)), Colour(0.25, 0.25, 0.25))
        self.assertEqual(pattern.pattern_at(Point(-1, 0, 0)), BLACK)

    def test_a_gradient_ring_repeats_in_both_x_and_z_directions(self):
        # Arrange
        val = 1 / (2 * sqrt(2))

        # Act
        pattern = GradientRingPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(val, 0, -val)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(1, 0, 0)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(-2 * val, 0, 2 * val)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(-3 * val, 0, -3 * val)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(5 * val, 0, 5 * val)), Colour(0.5, 0.5, 0.5))


class DoubleGradientRingPatternTestCase(unittest.TestCase):
    def test_double_gradient_ring_linearly_interpolates_in_both_x_and_z_directions_in_first_half(self):
        # Arrange

        # Act
        pattern = DoubleGradientRingPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0.125, 0, 0)), Colour(0.75, 0.75, 0.75))
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0.25)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(0, 0, -0.375)), Colour(0.25, 0.25, 0.25))
        self.assertEqual(pattern.pattern_at(Point(-0.5, 0, 0)), BLACK)

    def test_double_gradient_ring_linearly_interpolates_in_both_x_and_z_directions_in_second_half(self):
        # Arrange

        # Act
        pattern = DoubleGradientRingPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(1, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0.875)), Colour(0.75, 0.75, 0.75))
        self.assertEqual(pattern.pattern_at(Point(0, 0, -0.75)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(-0.625, 0, 0)), Colour(0.25, 0.25, 0.25))
        self.assertEqual(pattern.pattern_at(Point(0.5, 0, 0)), BLACK)

    def test_double_gradient_ring_repeats_in_both_x_and_z_directions(self):
        # Arrange
        val = 1 / (4 * sqrt(2))

        # Act
        pattern = DoubleGradientRingPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(val, 0, -val)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(0.5, 0, 0)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(-2 * val, 0, 2 * val)), BLACK)
        self.assertEqual(pattern.pattern_at(Point(-3 * val, 0, -3 * val)), Colour(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(0, 0, -1)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(5 * val, 0, 5 * val)), Colour(0.5, 0.5, 0.5))


class CheckersPatternTestCase(unittest.TestCase):
    def test_checkers_should_repeat_in_x(self):
        # Arrange

        # Act
        pattern = CheckersPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0.99, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(1.01, 0, 0)), BLACK)

    def test_checkers_should_repeat_in_y(self):
        # Arrange

        # Act
        pattern = CheckersPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 0.99, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 1.01, 0)), BLACK)

    def test_checkers_should_repeat_in_z(self):
        # Arrange

        # Act
        pattern = CheckersPattern(WHITE, BLACK)

        # Assert
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0.99)), WHITE)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 1.01)), BLACK)


class BlendedPatternTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ground = Plane()
        pattern1 = StripePattern(WHITE, BLACK)
        pattern2 = StripePattern(WHITE, BLACK)
        pattern2.transform = Matrix.rotation_y(pi / 2)
        ground_pattern = BlendedPattern(pattern1, pattern2)
        self.ground.material = Material()
        self.ground.material.pattern = ground_pattern

    def test_blended_stripes_at_right_angles_should_repeat_in_x(self):
        # Arrange
        GREY = Colour(0.5, 0.5, 0.5)

        # Act
        results1 = [self.ground.material.pattern.pattern_at_shape(self.ground, Point(x + 0.5, 0, 0.5))
                    for x in range(-5, 6)]
        results2 = [self.ground.material.pattern.pattern_at_shape(self.ground, Point(x + 0.5, 0, 1.5))
                    for x in range(-5, 6)]

        # Assert
        self.assertTrue(all([r == BLACK for i, r in enumerate(results1) if i == 0 % 2]))
        self.assertTrue(all([r == GREY for i, r in enumerate(results1) if i == 1 % 2]))
        self.assertTrue(all([r == GREY for i, r in enumerate(results2) if i == 0 % 2]))
        self.assertTrue(all([r == WHITE for i, r in enumerate(results2) if i == 1 % 2]))

    def test_blended_stripes_at_right_angles_should_repeat_in_z(self):
        # Arrange
        GREY = Colour(0.5, 0.5, 0.5)

        # Act
        results1 = [self.ground.material.pattern.pattern_at_shape(self.ground, Point(0.5, 0, x + 0.5))
                    for x in range(-5, 6)]
        results2 = [self.ground.material.pattern.pattern_at_shape(self.ground, Point(1.5, 0, x + 0.5))
                    for x in range(-5, 6)]

        # Assert
        self.assertTrue(all([r == WHITE for i, r in enumerate(results1) if i == 0 % 2]))
        self.assertTrue(all([r == GREY for i, r in enumerate(results1) if i == 1 % 2]))
        self.assertTrue(all([r == GREY for i, r in enumerate(results2) if i == 0 % 2]))
        self.assertTrue(all([r == BLACK for i, r in enumerate(results2) if i == 1 % 2]))


if __name__ == '__main__':
    unittest.main()

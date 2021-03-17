import unittest
from materials import Material
from primitives import Sphere
from tuples import *
from lights import PointLight
from patterns import *
from math import sqrt


class MaterialsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.s = Sphere()

    def test_the_default_material(self):
        # Arrange
        m = Material()

        # Act

        # Assert
        self.assertEqual(m.colour, Colour(1, 1, 1))
        self.assertEqual(m.ambient, 0.1)
        self.assertEqual(m.diffuse, 0.9)
        self.assertEqual(m.specular, 0.9)
        self.assertEqual(m.shininess, 200.0)

    def test_material_equality(self):
        # Arrange
        m1 = Material()
        m2 = Material()

        # Act

        # Assert
        self.assertEqual(m1, m2)

    def test_lighting_with_the_eye_between_the_light_and_the_surface(self):
        # Arrange
        m = Material()
        position = Point(0, 0, 0)
        eye_vec = Vector(0, 0, -1)
        normal_vec = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Colour(1, 1, 1))
        expected = Colour(1.9, 1.9, 1.9)

        # Act
        result = m.lighting(self.s, light, position, eye_vec, normal_vec)

        # Assert
        self.assertEqual(result, expected)

    def test_lighting_with_the_eye_between_the_light_and_the_surface_with_eye_offset_at_45_degrees(self):
        # Arrange
        m = Material()
        position = Point(0, 0, 0)
        eye_vec = Vector(0, sqrt(2) / 2, -sqrt(2) / 2)
        normal_vec = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Colour(1, 1, 1))
        expected = Colour(1.0, 1.0, 1.0)

        # Act
        result = m.lighting(self.s, light, position, eye_vec, normal_vec)

        # Assert
        self.assertEqual(result, expected)

    def test_lighting_with_the_eye_opposite_surface_with_light_offset_at_45_degrees(self):
        # Arrange
        m = Material()
        position = Point(0, 0, 0)
        eye_vec = Vector(0, 0, -1)
        normal_vec = Vector(0, 0, -1)
        light = PointLight(Point(0, 10, -10), Colour(1, 1, 1))
        val = 0.1 + 0.9 * sqrt(2) / 2
        expected = Colour(val, val, val)

        # Act
        result = m.lighting(self.s, light, position, eye_vec, normal_vec)

        # Assert
        self.assertEqual(result, expected)

    def test_lighting_with_the_eye_in_path_of_the_reflection_vector(self):
        # Arrange
        m = Material()
        position = Point(0, 0, 0)
        eye_vec = Vector(0, -sqrt(2) / 2, -sqrt(2) / 2)
        normal_vec = Vector(0, 0, -1)
        light = PointLight(Point(0, 10, -10), Colour(1, 1, 1))
        val = 0.1 + 0.9 * sqrt(2) / 2 + 0.9
        expected = Colour(val, val, val)

        # Act
        result = m.lighting(self.s, light, position, eye_vec, normal_vec)

        # Assert
        self.assertEqual(result, expected)

    def test_lighting_with_the_light_behind_the_surface(self):
        # Arrange
        m = Material()
        position = Point(0, 0, 0)
        eye_vec = Vector(0, 0, -1)
        normal_vec = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, 10), Colour(1, 1, 1))
        expected = Colour(0.1, 0.1, 0.1)

        # Act
        result = m.lighting(self.s, light, position, eye_vec, normal_vec)

        # Assert
        self.assertEqual(result, expected)

    def test_lighting_with_the_surface_in_shadow(self):
        # Arrange
        m = Material()
        position = Point(0, 0, 0)
        eye_vec = Vector(0, 0, -1)
        normal_vec = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Colour(1, 1, 1))
        in_shadow = True
        expected = Colour(0.1, 0.1, 0.1)

        # Act
        result = m.lighting(self.s, light, position, eye_vec, normal_vec, in_shadow)

        # Assert
        self.assertEqual(result, expected)

    def test_lighting_with_a_pattern_applied(self):
        # Arrange
        m = Material()
        m.pattern = StripePattern(WHITE, BLACK)
        m.ambient = 1
        m.diffuse = 0
        m.specular = 0
        eye_vec = Vector(0, 0, -1)
        normal_vec = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Colour(1, 1, 1))
        expected1 = Colour(1, 1, 1)
        expected2 = Colour(0, 0, 0)

        # Act
        result1 = m.lighting(self.s, light, Point(0.9, 0, 0), eye_vec, normal_vec)
        result2 = m.lighting(self.s, light, Point(1.1, 0, 0), eye_vec, normal_vec)

        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_the_default_material_has_a_reflective_property(self):
        # Arrange
        m = Material()

        # Act

        # Assert
        self.assertEqual(m.reflective, 0)

    def test_the_default_material_has_a_transparency_property(self):
        # Arrange
        m = Material()

        # Act

        # Assert
        self.assertEqual(m.transparency, 0)

    def test_the_default_material_has_a_refractive_index_property(self):
        # Arrange
        m = Material()

        # Act

        # Assert
        self.assertEqual(m.refractive_index, 1)

    def test_the_default_material_has_a_casts_shadow_property(self):
        # Arrange
        m = Material()

        # Act

        # Assert
        self.assertTrue(m.casts_shadow)

    def test_the_default_material_has_a_shadow_transmission_property(self):
        # Arrange
        m = Material()

        # Act

        # Assert
        self.assertEqual(m.shadow_transmission, 1)

    def test_the_default_material_has_zero_shadow_transmission_if_casts_shadow_is_false(self):
        # Arrange
        m = Material()

        # Act
        m.casts_shadow = False

        # Assert
        self.assertEqual(m.shadow_transmission, 0)

    def test_the_materials_will_stat_casting_shadows_if_shadow_transmission_is_set_above_zero(self):
        # Arrange
        m = Material()
        m.casts_shadow = False

        # Act
        m.shadow_transmission = 0.5

        # Assert
        self.assertTrue(m.casts_shadow)


if __name__ == '__main__':
    unittest.main()

import unittest
from matrices import Matrix
from tuples import *
from math import pi, sqrt


class MatricesTestCase(unittest.TestCase):
    EPSILON = 0.000001

    def test_creating_a_4_by_4_matrix(self):
        # Arrange

        # Act
        m = Matrix([[1, 2, 3, 4], [5.5, 6.5, 7.5, 8.5], [9, 10, 11, 12], [13.5, 14.5, 15.5, 16.5]])

        # Assert
        self.assertEqual(m.matrix[0, 0], 1)
        self.assertEqual(m.matrix[0, 3], 4)
        self.assertEqual(m.matrix[1, 0], 5.5)
        self.assertEqual(m.matrix[1, 2], 7.5)
        self.assertEqual(m.matrix[2, 2], 11)
        self.assertEqual(m.matrix[3, 0], 13.5)
        self.assertEqual(m.matrix[3, 2], 15.5)

    def test_creating_a_3_by_3_matrix(self):
        # Arrange

        # Act
        m = Matrix([[-3, 5, 0], [1, -2, -7], [0, 1, 1]])

        # Assert
        self.assertEqual(m.matrix[0, 0], -3)
        self.assertEqual(m.matrix[1, 1], -2)
        self.assertEqual(m.matrix[2, 2], 1)

    def test_creating_a_2_by_2_matrix(self):
        # Arrange

        # Act
        m = Matrix([[-3, 5], [1, -2]])

        # Assert
        self.assertEqual(m.matrix[0, 0], -3)
        self.assertEqual(m.matrix[0, 1], 5)
        self.assertEqual(m.matrix[1, 0], 1)
        self.assertEqual(m.matrix[1, 1], -2)

    def test_4_by_4_matrix_equality(self):
        # Arrange
        a = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
        b = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])

        # Act
        result = a == b

        # Assert
        self.assertTrue(result)

    def test_4_by_4_matrix_inequality(self):
        # Arrange
        a = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
        b = Matrix([[2, 3, 4, 5], [6, 7, 8, 9], [8, 7, 6, 5], [4, 3, 2, 1]])

        # Act
        result = a == b

        # Assert
        self.assertFalse(result)

    def test_4_by_4_matrix_multiplication(self):
        # Arrange
        a = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
        b = Matrix([[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]])
        expected = Matrix([[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]])

        # Act
        result = a * b

        # Assert
        self.assertEqual(result, expected)

    def test_multiplying_4_by_4_matrix_by_a_tuple(self):
        # Arrange
        a = Matrix([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
        b = Tuple(1, 2, 3, 1)
        expected = Tuple(18, 24, 33, 1)

        # Act
        result = a * b

        # Assert
        self.assertEqual(result, expected)

    def test_multiplying_4_by_4_matrix_by_identity_matrix(self):
        # Arrange
        a = Matrix([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
        b = Matrix.identity(4)

        # Act
        result = a * b

        # Assert
        self.assertEqual(result, a)

    def test_multiplying_4_by_4_identity_matrix_by_a_tuple(self):
        # Arrange
        a = Matrix.identity(4)
        b = Tuple(1, 2, 3, 1)

        # Act
        result = a * b

        # Assert
        self.assertEqual(result, b)

    def test_transposing_a_4_by_4_matrix(self):
        # Arrange
        a = Matrix([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
        expected = Matrix([[1, 2, 8, 0], [2, 4, 6, 0], [3, 4, 4, 0], [4, 2, 1, 1]])

        # Act
        result = a.transpose()

        # Assert
        self.assertEqual(result, expected)

    def test_transposing_the_4_by_4_identity_matrix(self):
        # Arrange
        a = Matrix.identity(4)

        # Act
        result = a.transpose()

        # Assert
        self.assertEqual(result, a)

    def test_slow_determinant_of_a_2_by_2_matrix(self):
        # Arrange
        a = Matrix([[1, 5], [-3, 2]])
        expected = 17

        # Act
        result = a.slow_determinant()

        # Assert
        self.assertEqual(result, expected)

    def test_determinant_of_a_2_by_2_matrix(self):
        # Arrange
        a = Matrix([[1, 5], [-3, 2]])
        expected = 17

        # Act
        result = a.determinant()

        # Assert
        self.assertEqual(result, expected)

    def test_submatrix_of_a_3_by_3_matrix_is_a_2_by_2_matrix(self):
        # Arrange
        a = Matrix([[1, 5, 0], [-3, 2, 7], [0, 6, -3]])
        expected = Matrix([[-3, 2], [0, 6]])

        # Act
        result = a.submatrix(0, 2)

        # Assert
        self.assertEqual(result, expected)

    def test_submatrix_of_a_4_by_4_matrix_is_a_3_by_3_matrix(self):
        # Arrange
        a = Matrix([[1, 5, 0, 6], [-3, 2, 7, -8], [0, 6, -3, 2], [-7, 1, -1, 1]])
        expected = Matrix([[1, 0, 6], [-3, 7, -8], [-7, -1, 1]])

        # Act
        result = a.submatrix(2, 1)

        # Assert
        self.assertEqual(result, expected)

    def test_calculate_minor_of_a_3_by_3_matrix(self):
        # Arrange
        a = Matrix([[3, 5, 0], [2, -1, -7], [6, -1, 5]])
        expected = 25

        # Act
        b = a.submatrix(1, 0)
        result1 = b.determinant()
        result2 = a.minor(1, 0)

        # Assert
        self.assertAlmostEqual(result1, expected, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(result2, expected, delta=self.__class__.EPSILON)

    def test_calculate_cofactors_of_a_3_by_3_matrix(self):
        # Arrange
        a = Matrix([[3, 5, 0], [2, -1, -7], [6, -1, 5]])
        e1 = -12
        e2 = -12
        e3 = 25
        e4 = -25

        # Act
        r1 = a.minor(0, 0)
        r2 = a.cofactor(0, 0)
        r3 = a.minor(1, 0)
        r4 = a.cofactor(1, 0)

        # Assert
        self.assertAlmostEqual(r1, e1, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r2, e2, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r3, e3, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r4, e4, delta=self.__class__.EPSILON)

    def test_calculate_slow_determinant_of_a_3_by_3_matrix(self):
        # Arrange
        a = Matrix([[1, 2, 6], [-5, 8, -4], [2, 6, 4]])
        e1 = 56
        e2 = 12
        e3 = -46
        e4 = -196

        # Act
        r1 = a.cofactor(0, 0)
        r2 = a.cofactor(0, 1)
        r3 = a.cofactor(0, 2)
        r4 = a.slow_determinant()

        # Assert
        self.assertAlmostEqual(r1, e1, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r2, e2, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r3, e3, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r4, e4, delta=self.__class__.EPSILON)

    def test_calculate_determinant_of_a_3_by_3_matrix(self):
        # Arrange
        a = Matrix([[1, 2, 6], [-5, 8, -4], [2, 6, 4]])
        expected = -196

        # Act
        result = a.determinant()

        # Assert
        self.assertAlmostEqual(result, expected, delta=self.__class__.EPSILON)

    def test_calculate_slow_determinant_of_a_4_by_4_matrix(self):
        # Arrange
        a = Matrix([[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
        e1 = 690
        e2 = 447
        e3 = 210
        e4 = 51
        e5 = -4071

        # Act
        r1 = a.cofactor(0, 0)
        r2 = a.cofactor(0, 1)
        r3 = a.cofactor(0, 2)
        r4 = a.cofactor(0, 3)
        r5 = a.slow_determinant()

        # Assert
        self.assertAlmostEqual(r1, e1, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r2, e2, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r3, e3, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r4, e4, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r5, e5, delta=self.__class__.EPSILON)

    def test_calculate_determinant_of_a_4_by_4_matrix(self):
        # Arrange
        a = Matrix([[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
        expected = -4071

        # Act
        result = a.determinant()

        # Assert
        self.assertAlmostEqual(result, expected, delta=self.__class__.EPSILON)

    def test_slow_inversion_of_a_4_by_4_invertible_matrix(self):
        # Arrange
        a = Matrix([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
        expected = -2120

        # Act
        result = a.slow_determinant()

        # Assert
        self.assertAlmostEqual(result, expected, delta=self.__class__.EPSILON)
        self.assertTrue(a.is_invertible)

    def test_inversion_of_a_4_by_4_invertible_matrix(self):
        # Arrange
        a = Matrix([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
        expected = -2120

        # Act
        result = a.determinant()

        # Assert
        self.assertAlmostEqual(result, expected, delta=self.__class__.EPSILON)
        self.assertTrue(a.is_invertible)

    def test_slow_inversion_of_a_4_by_4_noninvertible_matrix(self):
        # Arrange
        a = Matrix([[-4, 2, -2, -3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
        expected = 0

        # Act
        result = a.slow_determinant()

        # Assert
        self.assertAlmostEqual(result, expected, delta=self.__class__.EPSILON)
        self.assertFalse(a.is_invertible)

    def test_inversion_of_a_4_by_4_noninvertible_matrix(self):
        # Arrange
        a = Matrix([[-4, 2, -2, -3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
        expected = 0

        # Act
        result = a.determinant()

        # Assert
        self.assertAlmostEqual(result, expected, delta=self.__class__.EPSILON)
        self.assertFalse(a.is_invertible)

    def test_calculate_slow_inversion_of_a_4_by_4_invertible_matrix(self):
        # Arrange
        a = Matrix([[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]])
        expected_det = 532
        expected_inv = Matrix([[0.21805, 0.45113, 0.24060, -0.04511], [-0.80827, -1.45677, -0.44361, 0.52068],
                               [-0.07895, -0.22368, -0.05263, 0.19737], [-0.52256, -0.81391, -0.30075, 0.30639]])
        e1 = -160
        e2 = -160 / expected_det
        e3 = 105
        e4 = 105 / expected_det

        # Act
        result_inv = a.slow_inverse()
        result_det = a.slow_determinant()
        r1 = a.cofactor(2, 3)
        r2 = result_inv.matrix[3, 2]
        r3 = a.cofactor(3, 2)
        r4 = result_inv.matrix[2, 3]

        # Assert
        self.assertEqual(result_inv, expected_inv)
        self.assertAlmostEqual(result_det, expected_det, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r1, e1, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r2, e2, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r3, e3, delta=self.__class__.EPSILON)
        self.assertAlmostEqual(r4, e4, delta=self.__class__.EPSILON)

    def test_calculate_slow_inversion_of_a_4_by_4_invertible_matrix2(self):
        # Arrange
        a = Matrix([[8, -5, 9, 2], [7, 5, 6, 1], [-6, 0, 9, 6], [-3, 0, -9, -4]])
        expected_inv = Matrix([[-0.15385, -0.15385, -0.28205, -0.53846], [-0.07692, 0.12308, 0.02564, 0.03077],
                               [0.35897, 0.35897, 0.43590, 0.92308], [-0.69231, -0.69231, -0.76923, -1.92308]])

        # Act
        result_inv = a.slow_inverse()

        # Assert
        self.assertEqual(result_inv, expected_inv)

    def test_calculate_slow_inversion_of_a_4_by_4_invertible_matrix3(self):
        # Arrange
        a = Matrix([[9, 3, 0, 9], [-5, -2, -6, -3], [-4, 9, 6, 4], [-7, 6, 6, 2]])
        expected_inv = Matrix([[-0.04074, -0.07778, 0.14444, -0.22222], [-0.07778, 0.03333, 0.36667, -0.33333],
                               [-0.02901, -0.14630, -0.10926, 0.12963], [0.17778, 0.06667, -0.26667, 0.33333]])

        # Act
        result_inv = a.slow_inverse()

        # Assert
        self.assertEqual(result_inv, expected_inv)

    def test_calculate_inversion_of_a_4_by_4_invertible_matrix(self):
        # Arrange
        a = Matrix([[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]])
        expected_inv = Matrix([[0.21805, 0.45113, 0.24060, -0.04511], [-0.80827, -1.45677, -0.44361, 0.52068],
                               [-0.07895, -0.22368, -0.05263, 0.19737], [-0.52256, -0.81391, -0.30075, 0.30639]])

        # Act
        result_inv = a.inverse()

        # Assert
        self.assertEqual(result_inv, expected_inv)

    def test_calculate_inversion_of_a_4_by_4_invertible_matrix2(self):
        # Arrange
        a = Matrix([[8, -5, 9, 2], [7, 5, 6, 1], [-6, 0, 9, 6], [-3, 0, -9, -4]])
        expected_inv = Matrix([[-0.15385, -0.15385, -0.28205, -0.53846], [-0.07692, 0.12308, 0.02564, 0.03077],
                               [0.35897, 0.35897, 0.43590, 0.92308], [-0.69231, -0.69231, -0.76923, -1.92308]])

        # Act
        result_inv = a.inverse()

        # Assert
        self.assertEqual(result_inv, expected_inv)

    def test_calculate_inversion_of_a_4_by_4_invertible_matrix3(self):
        # Arrange
        a = Matrix([[9, 3, 0, 9], [-5, -2, -6, -3], [-4, 9, 6, 4], [-7, 6, 6, 2]])
        expected_inv = Matrix([[-0.04074, -0.07778, 0.14444, -0.22222], [-0.07778, 0.03333, 0.36667, -0.33333],
                               [-0.02901, -0.14630, -0.10926, 0.12963], [0.17778, 0.06667, -0.26667, 0.33333]])

        # Act
        result_inv = a.inverse()

        # Assert
        self.assertEqual(result_inv, expected_inv)

    def test_multiply_a_matrix_product_by_the_slow_inverse_returns_original_matrix(self):
        # Arrange
        a = Matrix([[3, -9,  7,  3], [3, -8,  2, -9], [-4,  4,  4,  1], [-6,  5, -1,  1]])
        b = Matrix([[8,  2,  2,  2], [3, -1,  7,  0], [7,  0,  5,  4], [6, -2,  0,  5]])

        # Act
        c = a * b
        result = c * b.slow_inverse()

        # Assert
        self.assertEqual(result, a)

    def test_multiply_a_matrix_product_by_the_inverse_returns_original_matrix(self):
        # Arrange
        a = Matrix([[3, -9,  7,  3], [3, -8,  2, -9], [-4,  4,  4,  1], [-6,  5, -1,  1]])
        b = Matrix([[8,  2,  2,  2], [3, -1,  7,  0], [7,  0,  5,  4], [6, -2,  0,  5]])

        # Act
        c = a * b
        result = c * b.inverse()

        # Assert
        self.assertEqual(result, a)

    def test_multiply_a_point_by_a_translation_matrix(self):
        # Arrange
        transform = Matrix.translation(5, -3, 2)
        p = Point(-3, 4, 5)
        expected = Point(2, 1, 7)

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_multiply_a_point_by_the_inverse_of_a_translation_matrix(self):
        # Arrange
        transform = Matrix.translation(5, -3, 2)
        inverse = transform.inverse()
        p = Point(-3, 4, 5)
        expected = Point(-8, 7, 3)

        # Act
        result = inverse * p

        # Assert
        self.assertEqual(result, expected)

    def test_multiplying_a_vector_by_a_translation_matrix_has_no_effect(self):
        # Arrange
        transform = Matrix.translation(5, -3, 2)
        v = Vector(-3, 4, 5)

        # Act
        result = transform * v

        # Assert
        self.assertEqual(result, v)

    def test_multiply_a_point_by_a_scaling_matrix(self):
        # Arrange
        transform = Matrix.scaling(2, 3, 4)
        p = Point(-4, 6, 8)
        expected = Point(-8, 18, 32)

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_multiply_a_vector_by_a_scaling_matrix(self):
        # Arrange
        transform = Matrix.scaling(2, 3, 4)
        v = Vector(-4, 6, 8)
        expected = Vector(-8, 18, 32)

        # Act
        result = transform * v

        # Assert
        self.assertEqual(result, expected)

    def test_multiply_a_vector_by_the_inverse_of_a_scaling_matrix(self):
        # Arrange
        transform = Matrix.scaling(2, 3, 4)
        inverse = transform.inverse()
        v = Vector(-4, 6, 8)
        expected = Vector(-2, 2, 2)

        # Act
        result = inverse * v

        # Assert
        self.assertEqual(result, expected)

    def test_reflection_is_scaling_by_a_negative_value(self):
        # Arrange
        transform = Matrix.scaling(-1, 1, 1)
        p = Point(2, 3, 4)
        expected = Point(-2, 3, 4)

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_rotating_a_point_around_the_x_axis(self):
        # Arrange
        p = Point(0, 1, 0)
        half_quarter = Matrix.rotation_x(pi / 4)
        full_quarter = Matrix.rotation_x(pi / 2)
        expected1 = Point(0, sqrt(2) / 2, sqrt(2) / 2)
        expected2 = Point(0, 0, 1)

        # Act
        result1 = half_quarter * p
        result2 = full_quarter * p

        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_the_inverse_of_an_x_rotation_rotates_in_the_opposite_direction(self):
        # Arrange
        p = Point(0, 1, 0)
        half_quarter = Matrix.rotation_x(pi / 4)
        inverse = half_quarter.inverse()
        expected = Point(0, sqrt(2) / 2, -sqrt(2) / 2)

        # Act
        result = inverse * p

        # Assert
        self.assertEqual(result, expected)

    def test_rotating_a_point_around_the_y_axis(self):
        # Arrange
        p = Point(0, 0, 1)
        half_quarter = Matrix.rotation_y(pi / 4)
        full_quarter = Matrix.rotation_y(pi / 2)
        expected1 = Point(sqrt(2) / 2, 0, sqrt(2) / 2)
        expected2 = Point(1, 0, 0)

        # Act
        result1 = half_quarter * p
        result2 = full_quarter * p

        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_rotating_a_point_around_the_z_axis(self):
        # Arrange
        p = Point(0, 1, 0)
        half_quarter = Matrix.rotation_z(pi / 4)
        full_quarter = Matrix.rotation_z(pi / 2)
        expected1 = Point(-sqrt(2) / 2, sqrt(2) / 2, 0)
        expected2 = Point(-1, 0, 0)

        # Act
        result1 = half_quarter * p
        result2 = full_quarter * p

        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_a_shearing_transformation_which_moves_x_in_proportion_to_y(self):
        # Arrange
        p = Point(2, 3, 4)
        transform = Matrix.shearing(1, 0, 0, 0, 0, 0)
        expected = Point(5, 3, 4)       # x is moved by 1*y

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_a_shearing_transformation_which_moves_x_in_proportion_to_z(self):
        # Arrange
        p = Point(2, 3, 4)
        transform = Matrix.shearing(0, 1, 0, 0, 0, 0)
        expected = Point(6, 3, 4)       # x is moved by 1*z

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_a_shearing_transformation_which_moves_y_in_proportion_to_x(self):
        # Arrange
        p = Point(2, 3, 4)
        transform = Matrix.shearing(0, 0, 1, 0, 0, 0)
        expected = Point(2, 5, 4)       # y is moved by 1*x

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_a_shearing_transformation_which_moves_y_in_proportion_to_z(self):
        # Arrange
        p = Point(2, 3, 4)
        transform = Matrix.shearing(0, 0, 0, 1, 0, 0)
        expected = Point(2, 7, 4)       # y is moved by 1*z

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_a_shearing_transformation_which_moves_z_in_proportion_to_x(self):
        # Arrange
        p = Point(2, 3, 4)
        transform = Matrix.shearing(0, 0, 0, 0, 1, 0)
        expected = Point(2, 3, 6)       # z is moved by 1*x

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_a_shearing_transformation_which_moves_z_in_proportion_to_y(self):
        # Arrange
        p = Point(2, 3, 4)
        transform = Matrix.shearing(0, 0, 0, 0, 0, 1)
        expected = Point(2, 3, 7)       # z is moved by 1*y

        # Act
        result = transform * p

        # Assert
        self.assertEqual(result, expected)

    def test_individual_transformations_are_applied_in_sequence(self):
        # Arrange
        p = Point(1, 0, 1)
        rot = Matrix.rotation_x(pi / 2)
        sca = Matrix.scaling(5, 5, 5)
        tra = Matrix.translation(10, 5, 7)
        exp_rot = Point(1, -1, 0)
        exp_sca = Point(5, -5, 0)
        exp_tra = Point(15, 0, 7)

        # Act
        res_rot = rot * p
        res_sca = sca * res_rot
        res_tra = tra * res_sca

        # Assert
        self.assertEqual(res_rot, exp_rot)
        self.assertEqual(res_sca, exp_sca)
        self.assertEqual(res_tra, exp_tra)

    def test_chained_transformations_are_applied_reverse_order(self):
        # Arrange
        p = Point(1, 0, 1)
        rot = Matrix.rotation_x(pi / 2)
        sca = Matrix.scaling(5, 5, 5)
        tra = Matrix.translation(10, 5, 7)
        expected = Point(15, 0, 7)

        # Act
        translation = tra * sca * rot
        result = translation * p

        # Assert
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

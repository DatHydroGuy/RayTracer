import numpy as np
from tuples import Tuple
from math import sin, cos


class Matrix:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)
        self.is_invertible = None

    def __eq__(self, other):
        return np.allclose(self.matrix, other.matrix, rtol=0.0001)

    def __mul__(self, other):
        if type(other) is Matrix:
            result = np.matmul(self.matrix, other.matrix)
            return Matrix(result.tolist())
        else:
            result = self.matrix.dot(other.vec)
            return Tuple(*result.tolist())

    @staticmethod
    def identity(size):
        return Matrix(np.identity(size).tolist())

    def transpose(self):
        return Matrix(np.transpose(self.matrix).tolist())

    def determinant(self):
        result = np.linalg.det(self.matrix)
        self.is_invertible = result != 0
        return result

    def slow_determinant(self):
        if self.matrix.shape == (2, 2):
            result = self.matrix[0, 0] * self.matrix[1, 1] - self.matrix[0, 1] * self.matrix[1, 0]
        else:
            result = 0
            for ic, col in enumerate(self.matrix[0]):
                result += col * self.cofactor(0, ic)

        self.is_invertible = result != 0
        return result

    def submatrix(self, row, column):
        return Matrix(np.delete(np.delete(self.matrix, row, axis=0), column, axis=1))

    def minor(self, row, column):
        return self.submatrix(row, column).determinant()

    def cofactor(self, row, column):
        factor = 1 if (row + column) % 2 == 0 else -1
        return factor * self.minor(row, column)

    def slow_inverse(self):
        determinant = self.slow_determinant()
        if not self.is_invertible:
            return None

        new = np.empty(self.matrix.shape, dtype=float)
        for row in range(self.matrix.shape[0]):
            for col in range(self.matrix.shape[1]):
                new[col, row] = self.cofactor(row, col) / determinant

        return Matrix(new.tolist())

    def inverse(self):
        return Matrix(np.linalg.inv(self.matrix).tolist())

    @staticmethod
    def translation(x, y, z):
        ident = Matrix.identity(4)
        ident.matrix[0, 3] = x
        ident.matrix[1, 3] = y
        ident.matrix[2, 3] = z
        return ident

    @staticmethod
    def scaling(x, y, z):
        ident = Matrix.identity(4)
        ident.matrix[0, 0] = x
        ident.matrix[1, 1] = y
        ident.matrix[2, 2] = z
        return ident

    @staticmethod
    def rotation_x(radians):
        ident = Matrix.identity(4)
        ident.matrix[1, 1] = cos(radians)
        ident.matrix[1, 2] = -sin(radians)
        ident.matrix[2, 1] = sin(radians)
        ident.matrix[2, 2] = cos(radians)
        return ident

    @staticmethod
    def rotation_y(radians):
        ident = Matrix.identity(4)
        ident.matrix[0, 0] = cos(radians)
        ident.matrix[0, 2] = sin(radians)
        ident.matrix[2, 0] = -sin(radians)
        ident.matrix[2, 2] = cos(radians)
        return ident

    @staticmethod
    def rotation_z(radians):
        ident = Matrix.identity(4)
        ident.matrix[0, 0] = cos(radians)
        ident.matrix[0, 1] = -sin(radians)
        ident.matrix[1, 0] = sin(radians)
        ident.matrix[1, 1] = cos(radians)
        return ident

    @staticmethod
    def shearing(xy, xz, yx, yz, zx, zy):
        ident = Matrix.identity(4)
        ident.matrix[0, 1] = xy
        ident.matrix[0, 2] = xz
        ident.matrix[1, 0] = yx
        ident.matrix[1, 2] = yz
        ident.matrix[2, 0] = zx
        ident.matrix[2, 1] = zy
        return ident

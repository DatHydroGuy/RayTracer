import numpy as np
from math import fabs


class Tuple:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.vec = np.array([x, y, z, w])
        self.is_point = w == 1.0
        self.is_vector = w == 0.0
        self.mag = np.linalg.norm(self.vec)
        self.norm = self.vec / self.mag if self.mag != 0 else float('inf')

    def __eq__(self, other, epsilon=0.00001):
        return fabs(self.x - other.x) < epsilon and \
            fabs(self.y - other.y) < epsilon and \
            fabs(self.z - other.z) < epsilon and \
            fabs(self.w - other.w) < epsilon

    def __add__(self, other):
        return Tuple(*(self.vec + other.vec))

    def __sub__(self, other):
        return Tuple(*(self.vec - other.vec))

    def __neg__(self):
        return Tuple(*(np.zeros(4) - self.vec))

    def __mul__(self, other):
        return Tuple(*(other * self.vec))

    def __truediv__(self, other):
        return Tuple(*(self.vec / other))

    def normalise(self):
        return self.norm

    def dot(self, other):
        return np.dot(self.vec, other.vec)


class Point(Tuple):
    def __init__(self, x, y, z):
        Tuple.__init__(self, x, y, z, 1.0)

    @classmethod
    def from_tuple(cls, in_tuple):
        return cls(in_tuple.x, in_tuple.y, in_tuple.z)


class Vector(Tuple):
    def __init__(self, x, y, z):
        Tuple.__init__(self, x, y, z, 0.0)

    def __mul__(self, other):
        return Vector(*(self.vec[:3] * other))

    def __rmul__(self, other):
        return Vector(*(self.vec[:3] * other))

    @classmethod
    def from_tuple(cls, in_tuple):
        return cls(in_tuple.x, in_tuple.y, in_tuple.z)

    def normalise(self):
        return Vector(self.norm[0], self.norm[1], self.norm[2])

    def cross(self, other):
        cross_tuple = np.cross(self.vec[:3], other.vec[:3])
        return Vector(cross_tuple[0], cross_tuple[1], cross_tuple[2])

    def reflect(self, normal):
        refl = self - normal * 2 * self.dot(normal)
        return Vector.from_tuple(refl)

from colours import Colour
from math import floor, sqrt
from matrices import Matrix
from abc import ABC, abstractmethod
from noise import pnoise3
from tuples import Point


BLACK = Colour(0, 0, 0)
WHITE = Colour(1, 1, 1)


class Pattern(ABC):
    a = None
    b = None
    _transform = Matrix.identity(4)
    _transform_inverse = Matrix.identity(4)

    def __init__(self, colour_a, colour_b):
        self.a = colour_a
        self.b = colour_b

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, value):
        self._transform = value
        self._transform_inverse = self.transform.inverse()

    @property
    def transform_inverse(self):
        return self._transform_inverse

    @transform_inverse.setter
    def transform_inverse(self, value):
        self._transform_inverse = value
        self._transform = self.transform_inverse.inverse()

    @abstractmethod
    def pattern_at(self, point):
        pass

    @abstractmethod
    def pattern_at_shape(self, shape, point):
        obj_point = shape.transform_inverse * point
        pattern_point = self._transform_inverse * obj_point
        return self.pattern_at(pattern_point)


class StripePattern(Pattern):
    def __init__(self, colour_a, colour_b):
        Pattern.__init__(self, colour_a, colour_b)

    def pattern_at(self, point):
        return self.a if floor(point.x) % 2 == 0 else self.b

    def pattern_at_shape(self, obj, world_point):
        return super(StripePattern, self).pattern_at_shape(obj, world_point)


class GradientPattern(Pattern):
    def __init__(self, colour_a, colour_b):
        Pattern.__init__(self, colour_a, colour_b)

    def pattern_at(self, point):
        distance = self.b - self.a
        fraction = point.x - floor(point.x)
        return self.b if point.x == 1 else self.a + distance * fraction

    def pattern_at_shape(self, obj, world_point):
        return super(GradientPattern, self).pattern_at_shape(obj, world_point)


class DoubleGradientPattern(Pattern):
    def __init__(self, colour_a, colour_b):
        Pattern.__init__(self, colour_a, colour_b)

    def pattern_at(self, point):
        distance = self.b - self.a
        fraction = 1 - abs((point.x - floor(point.x) - 0.5) * 2)
        return self.a if point.x == 1 else self.a + distance * fraction

    def pattern_at_shape(self, obj, world_point):
        return super(DoubleGradientPattern, self).pattern_at_shape(obj, world_point)


class RingPattern(Pattern):
    def __init__(self, colour_a, colour_b):
        Pattern.__init__(self, colour_a, colour_b)

    def pattern_at(self, point):
        return self.a if floor(sqrt(point.x * point.x + point.z * point.z)) % 2 == 0 else self.b

    def pattern_at_shape(self, obj, world_point):
        return super(RingPattern, self).pattern_at_shape(obj, world_point)


class GradientRingPattern(Pattern):
    def __init__(self, colour_a, colour_b):
        Pattern.__init__(self, colour_a, colour_b)

    def pattern_at(self, point):
        distance = self.b - self.a
        point_dist = sqrt(point.x * point.x + point.z * point.z)
        fraction = point_dist - floor(point_dist)
        return self.b if point_dist == 1 else self.a + distance * fraction

    def pattern_at_shape(self, obj, world_point):
        return super(GradientRingPattern, self).pattern_at_shape(obj, world_point)


class DoubleGradientRingPattern(Pattern):
    def __init__(self, colour_a, colour_b):
        Pattern.__init__(self, colour_a, colour_b)

    def pattern_at(self, point):
        distance = self.b - self.a
        point_dist = sqrt(point.x * point.x + point.z * point.z)
        fraction = 1 - abs((point_dist - floor(point_dist) - 0.5) * 2)
        return self.a if point_dist == 1 else self.a + distance * fraction

    def pattern_at_shape(self, obj, world_point):
        return super(DoubleGradientRingPattern, self).pattern_at_shape(obj, world_point)


class CheckersPattern(Pattern):
    def __init__(self, colour_a, colour_b):
        Pattern.__init__(self, colour_a, colour_b)

    def pattern_at(self, point):
        return self.a if (floor(point.x) + floor(point.y) + floor(point.z)) % 2 == 0 else self.b

    def pattern_at_shape(self, obj, world_point):
        return super(CheckersPattern, self).pattern_at_shape(obj, world_point)


class BlendedPattern(Pattern):
    def __init__(self, pattern_a, pattern_b):
        self.obj = None
        Pattern.__init__(self, pattern_a, pattern_b)

    def pattern_at(self, point):
        obj_point = self.obj.transform_inverse * point
        pattern_point_a = self.a.transform_inverse * obj_point
        pattern_point_b = self.b.transform_inverse * obj_point
        return Colour.from_tuple((self.a.pattern_at(pattern_point_a) + self.b.pattern_at(pattern_point_b)) / 2)

    def pattern_at_shape(self, obj, world_point):
        self.obj = obj
        return super(BlendedPattern, self).pattern_at_shape(obj, world_point)


class NestedPattern(Pattern):
    def __init__(self, parent_pattern, pattern_a, pattern_b):
        self.obj = None
        self.parent_pattern = parent_pattern
        Pattern.__init__(self, pattern_a, pattern_b)

    def pattern_at(self, point):
        obj_point = self.obj.transform_inverse * point
        pattern_point = self.parent_pattern.transform_inverse * obj_point
        parent_pattern_point = self.parent_pattern.pattern_at(pattern_point)
        pattern_point_a = self.a.transform_inverse * obj_point
        pattern_point_b = self.b.transform_inverse * obj_point
        return Colour.from_tuple(self.a.pattern_at(pattern_point_a)) if parent_pattern_point == self.parent_pattern.a \
            else Colour.from_tuple(self.b.pattern_at(pattern_point_b))

    def pattern_at_shape(self, obj, world_point):
        self.obj = obj
        return super(NestedPattern, self).pattern_at_shape(obj, world_point)


class PerturbedPattern(Pattern):
    def __init__(self, pattern_to_perturb, scale=0.4, octaves=1, persistence=0.5, lacunarity=2):
        self.pattern = pattern_to_perturb
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        Pattern.__init__(self, pattern_to_perturb.a, pattern_to_perturb.b)
        self.transform = pattern_to_perturb.transform

    def pattern_at(self, point):
        new_x = point.x + pnoise3(point.x, point.y + 1, point.z + 1, octaves=self.octaves,
                                  persistence=self.persistence, lacunarity=self.lacunarity) * self.scale
        new_y = point.y + pnoise3(point.x + 1, point.y, point.z + 1, octaves=self.octaves,
                                  persistence=self.persistence, lacunarity=self.lacunarity) * self.scale
        new_z = point.z + pnoise3(point.x + 1, point.y + 1, point.z, octaves=self.octaves,
                                  persistence=self.persistence, lacunarity=self.lacunarity) * self.scale
        return self.pattern.pattern_at(Point(new_x, new_y, new_z))

    def pattern_at_shape(self, obj, world_point):
        return super(PerturbedPattern, self).pattern_at_shape(obj, world_point)

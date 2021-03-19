from tuples import *
from uuid import uuid4
from math import sqrt
from intersections import Intersection
from matrices import Matrix
from materials import Material
from abc import ABC, abstractmethod


class Shape(ABC):
    EPSILON = 0.00001
    _saved_ray = None
    _transform = None
    _transform_inverse = None

    def __init__(self, x=0, y=0, z=0):
        self.origin = Point(x, y, z)
        self.id = uuid4().hex
        self._transform = Matrix.identity(4)
        self._transform_inverse = Matrix.identity(4)
        self.material = Material()

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

    @property
    def saved_ray(self):
        return self._saved_ray

    @saved_ray.setter
    def saved_ray(self, value):
        self._saved_ray = value

    @abstractmethod
    def intersects(self, ray):
        self._saved_ray = ray.transform(self._transform_inverse)
        return self.local_intersect(self._saved_ray)

    @abstractmethod
    def local_intersect(self, local_ray):
        pass

    @abstractmethod
    def normal_at(self, point):
        object_point = self._transform_inverse * point
        object_normal = self.local_normal_at(object_point)
        world_normal = self._transform_inverse.transpose() * object_normal
        world_normal.w = 0
        return Vector.from_tuple(world_normal).normalise()

    @abstractmethod
    def local_normal_at(self, local_point):
        pass

    def set_transform(self, new_transform):
        self.transform = new_transform


class Sphere(Shape):
    def __init__(self, x=0, y=0, z=0):
        Shape.__init__(self, x, y, z)

    def __eq__(self, other, epsilon=0.00001):
        return self.origin == other.origin and \
               self.transform == other.transform and \
               self.material == other.material

    @classmethod
    def from_point(cls, point, r=1):
        """Initialize sphere from a point and radius"""
        return cls(point.x, point.y, point.z)

    @classmethod
    def glass_sphere(cls):
        s = cls()
        s.material.transparency = 1
        s.material.refractive_index = 1.5
        return s

    def intersects(self, ray):
        return super().intersects(ray)

    def local_intersect(self, local_ray):
        primitive_to_ray = local_ray.origin - self.origin
        a = local_ray.direction.dot(local_ray.direction)
        b = 2 * local_ray.direction.dot(primitive_to_ray)
        c = primitive_to_ray.dot(primitive_to_ray) - 1
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return []
        else:
            t1 = (-b - sqrt(discriminant)) / (2 * a)
            t2 = (-b + sqrt(discriminant)) / (2 * a)
            return [Intersection(t1, self), Intersection(t2, self)]

    def normal_at(self, world_point):
        return super(Sphere, self).normal_at(world_point)

    def local_normal_at(self, object_point):
        return Vector.from_tuple(object_point - Point(0, 0, 0))


class Plane(Shape):
    def __init__(self, x=0, y=0, z=0):
        Shape.__init__(self, x, y, z)

    def __eq__(self, other, epsilon=0.00001):
        return self.origin == other.origin and \
               self.transform == other.transform and \
               self.material == other.material

    def intersects(self, ray):
        return super().intersects(ray)

    def local_intersect(self, local_ray):
        if abs(local_ray.direction.y) < self.EPSILON:
            return []
        else:
            t = -local_ray.origin.y / local_ray.direction.y
            return [Intersection(t, self)]

    def normal_at(self, world_point):
        return super(Plane, self).normal_at(world_point)

    def local_normal_at(self, object_point):
        return Vector(0, 1, 0)


class Cube(Shape):
    def __init__(self, x=0, y=0, z=0):
        Shape.__init__(self, x, y, z)

    def __eq__(self, other, epsilon=0.00001):
        return self.origin == other.origin and \
               self.transform == other.transform and \
               self.material == other.material

    def check_axis(self, origin, direction):
        t_min_numerator = -1 - origin
        t_max_numerator = 1 - origin

        if fabs(direction) >= self.EPSILON:
            t_min = t_min_numerator / direction
            t_max = t_max_numerator / direction
        else:
            t_min = t_min_numerator * float('inf')
            t_max = t_max_numerator * float('inf')

        return min(t_min, t_max), max(t_min, t_max)

    def intersects(self, ray):
        return super().intersects(ray)

    def local_intersect(self, local_ray):
        x_tmin, x_tmax = self.check_axis(local_ray.origin.x, local_ray.direction.x)
        y_tmin, y_tmax = self.check_axis(local_ray.origin.y, local_ray.direction.y)
        z_tmin, z_tmax = self.check_axis(local_ray.origin.z, local_ray.direction.z)
        t_min = max(x_tmin, y_tmin, z_tmin)
        t_max = min(x_tmax, y_tmax, z_tmax)
        return [Intersection(t_min, self), Intersection(t_max, self)] if t_min <= t_max else []

    def normal_at(self, world_point):
        return super(Cube, self).normal_at(world_point)

    def local_normal_at(self, object_point):
        max_x = fabs(object_point.x)
        max_y = fabs(object_point.y)
        max_z = fabs(object_point.z)
        max_dir = max(max_x, max_y, max_z)

        if max_dir == max_x:
            return Vector(object_point.x, 0, 0)
        elif max_dir == max_y:
            return Vector(0, object_point.y, 0)
        else:
            return Vector(0, 0, object_point.z)

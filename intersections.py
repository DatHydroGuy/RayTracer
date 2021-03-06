from dataclasses import dataclass
from tuples import *
from math import sqrt


@dataclass
class Comps:
    """Class for pre-computed intersection state values"""
    t: float = None
    object: object = None
    point: Point = None
    eye_vector: Vector = None
    normal_vector: Vector = None
    reflect_vector: Vector = None
    inside: bool = None
    over_point: Point = None
    under_point: Point = None
    n1: float = 0.0
    n2: float = 0.0


class Intersection:
    EPSILON = 0.00001

    def __init__(self, t, intersect_object):
        self.t = t
        self.object = intersect_object

    def __lt__(self, other):
        return self.t < other.t

    def prepare_computations(self, ray, all_intersections=None):
        comps = Comps()
        comps.t = self.t
        comps.object = self.object
        comps.point = ray.position(self.t)
        comps.eye_vector = -ray.direction
        comps.normal_vector = comps.object.normal_at(comps.point)
        comps.reflect_vector = ray.direction.reflect(comps.normal_vector)
        if comps.normal_vector.dot(comps.eye_vector) < 0:
            comps.inside = True
            comps.normal_vector = -comps.normal_vector
        else:
            comps.inside = False
        comps.over_point = Point.from_tuple(comps.point + comps.normal_vector * self.EPSILON)
        comps.under_point = Point.from_tuple(comps.point - comps.normal_vector * self.EPSILON)
        if all_intersections is None:
            all_intersections = [self]
        comps.n1, comps.n2 = self.calculate_refractive_normals(all_intersections)
        return comps

    def calculate_refractive_normals(self, intersection_list):
        containers = []
        n1 = 1
        n2 = 1
        for intersect in intersection_list:
            if fabs(intersect.t - self.t) < self.EPSILON:
                if len(containers) > 0:
                    n1 = containers[-1].material.refractive_index
            if intersect.object in containers:
                containers.remove(intersect.object)
            else:
                containers.append(intersect.object)
            if fabs(intersect.t - self.t) < self.EPSILON:
                if len(containers) > 0:
                    n2 = containers[-1].material.refractive_index
        return n1, n2

    @staticmethod
    def intersections(*args):
        intersection_list = []
        for arg in args:
            intersection_list.append(arg)
        return sorted(intersection_list)

    @staticmethod
    def hit(intersection_list):
        viables = [i for i in intersection_list if i.t >= 0]
        return min(viables) if len(viables) > 0 else None

    @staticmethod
    def schlick(comps):
        cosine = comps.eye_vector.dot(comps.normal_vector)
        if comps.n1 > comps.n2:
            n = comps.n1 / comps.n2
            sin_theta_t_squared = n * n * (1 - cosine * cosine)
            if sin_theta_t_squared > 1:
                return 1
            cosine = sqrt(1 - sin_theta_t_squared)

        r0 = ((comps.n1 - comps.n2) / (comps.n1 + comps.n2)) ** 2
        return r0 + (1 - r0) * (1 - cosine) ** 5

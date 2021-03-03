from dataclasses import dataclass
from tuples import *


@dataclass
class Comps:
    """Class for pre-computed intersection state values"""
    t: float = None
    object: object = None
    point: Point = None
    eye_vector: Vector = None
    normal_vector: Vector = None
    inside: bool = None
    over_point: Point = None


class Intersection:
    EPSILON = 0.00001

    def __init__(self, t, intersect_object):
        self.t = t
        self.object = intersect_object

    def __lt__(self, other):
        return self.t < other.t

    def prepare_computations(self, ray):
        comps = Comps()
        comps.t = self.t
        comps.object = self.object
        comps.point = ray.position(self.t)
        comps.eye_vector = -ray.direction
        comps.normal_vector = comps.object.normal_at(comps.point)
        if comps.normal_vector.dot(comps.eye_vector) < 0:
            comps.inside = True
            comps.normal_vector = -comps.normal_vector
        else:
            comps.inside = False
        comps.over_point = comps.point + comps.normal_vector * self.EPSILON
        return comps

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

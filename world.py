from primitives import Sphere
from colours import Colour
from matrices import Matrix
from lights import PointLight
from tuples import *
from rays import Ray
from intersections import Intersection
from math import sqrt


class World:
    def __init__(self):
        self.objects = []
        self.lights = []

    def intersect_world(self, ray):
        intersections = []
        for obj in self.objects:
            intersections.append(obj.intersects(ray))
        flattened_intersections = World.flatten(intersections)
        return sorted(flattened_intersections, key=lambda x: x.t)

    def shade_hit(self, comps, remaining=5):
        base_colour = Colour(0, 0, 0)
        for light in self.lights:
            shadowed = self.is_shadowed(comps.over_point, light)
            base_colour += comps.object.material.lighting(comps.object, light, comps.over_point, comps.eye_vector,
                                                          comps.normal_vector, shadowed)
            reflected = self.reflected_colour(comps, remaining)
            refracted = self.refracted_colour(comps, remaining)
            material = comps.object.material
            if material.reflective > 0 and material.transparency > 0:
                reflectance = Intersection.schlick(comps)
                return base_colour + reflected * reflectance + refracted * (1 - reflectance)
            else:
                return base_colour + reflected + refracted
        return base_colour

    def colour_at(self, ray, remaining=5):
        intersections = self.intersect_world(ray)
        hits = [i for i in intersections if i.t >= 0]
        if len(hits) == 0:
            return Colour(0, 0, 0)
        else:
            hit = min(hits)
            comps = hit.prepare_computations(ray, intersections)
            return self.shade_hit(comps, remaining)

    def is_shadowed(self, point, light=None):
        if light is None:
            light = self.lights[0]

        v = Vector.from_tuple(light.position - point)
        distance = v.mag
        direction = v.normalise()

        r = Ray(point, direction)
        intersections = self.intersect_world(r)

        h = Intersection.hit(intersections)
        if h is not None and h.t < distance and h.object.casts_shadow:
            return True
        else:
            return False

    def reflected_colour(self, comps, remaining=5):
        if comps.object.material.reflective == 0 or remaining < 1:
            return Colour(0, 0, 0)
        else:
            reflect_ray = Ray(comps.over_point, comps.reflect_vector)
            colour = self.colour_at(reflect_ray, remaining - 1)
            return colour * comps.object.material.reflective

    def refracted_colour(self, comps, remaining=5):
        if comps.object.material.transparency == 0 or remaining < 1:
            return Colour(0, 0, 0)
        else:
            n_ratio = comps.n1 / comps.n2
            cos_theta_i = comps.eye_vector.dot(comps.normal_vector)
            sin_theta_t_squared = n_ratio * n_ratio * (1 - cos_theta_i * cos_theta_i)
            if sin_theta_t_squared > 1:
                return Colour(0, 0, 0)
            else:
                cos_theta_t = sqrt(1 - sin_theta_t_squared)
                direction = comps.normal_vector * (n_ratio * cos_theta_i - cos_theta_t) - comps.eye_vector * n_ratio
                refract_ray = Ray(Point.from_tuple(comps.under_point), Vector.from_tuple(direction))
                colour = self.colour_at(refract_ray, remaining - 1)
                return colour * comps.object.material.transparency

    @staticmethod
    def flatten(list_of_lists):
        return [item for sublist in list_of_lists for item in sublist]

    @classmethod
    def default_world(cls):
        w = cls()
        s1 = Sphere()
        s1.material.colour = Colour(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular = 0.2
        w.objects.append(s1)
        s2 = Sphere()
        s2.transform = Matrix.scaling(0.5, 0.5, 0.5)
        w.objects.append(s2)
        w.lights.append(PointLight(Point(-10, 10, -10), Colour(1, 1, 1)))
        return w

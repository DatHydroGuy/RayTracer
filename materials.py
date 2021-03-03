from colours import Colour
from tuples import *
from math import fabs


class Material:
    def __init__(self, colour=None, ambient=None, diffuse=None, specular=None, shininess=None):
        self.colour = Colour(1, 1, 1) if colour is None else colour
        self.ambient = 0.1 if ambient is None else ambient
        self.diffuse = 0.9 if diffuse is None else diffuse
        self.specular = 0.9 if specular is None else specular
        self.shininess = 200.0 if shininess is None else shininess
        self.pattern = None

    def __eq__(self, other, epsilon=0.00001):
        return fabs(self.colour.red - other.colour.red) < epsilon and \
               fabs(self.colour.green - other.colour.green) < epsilon and \
               fabs(self.colour.blue - other.colour.blue) < epsilon and \
               fabs(self.ambient - other.ambient) < epsilon and \
               fabs(self.diffuse - other.diffuse) < epsilon and \
               fabs(self.specular - other.specular) < epsilon and \
               fabs(self.shininess - other.shininess) < epsilon

    def lighting(self, obj, light, point, eye_vector, normal_vector, in_shadow=False):
        colour = self.pattern.pattern_at_shape(obj, point) if self.pattern is not None else self.colour
        effective_colour = colour * light.intensity
        light_vector = Vector.from_tuple(light.position - point).normalise()
        ambient = effective_colour * self.ambient
        light_dot_normal = light_vector.dot(normal_vector)

        if light_dot_normal < 0 or in_shadow is True:
            return ambient
        else:
            diffuse = effective_colour * self.diffuse * light_dot_normal
            reflect_vector = -light_vector.reflect(normal_vector)
            reflect_dot_eye = reflect_vector.dot(eye_vector)

            if reflect_dot_eye <= 0:
                specular = Colour(0, 0, 0)
            else:
                factor = reflect_dot_eye ** self.shininess
                specular = light.intensity * self.specular * factor

            return ambient + diffuse + specular

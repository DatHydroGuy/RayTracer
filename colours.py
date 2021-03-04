from tuples import Vector
from math import fabs


class Colour(Vector):
    def __init__(self, red, green, blue):
        Vector.__init__(self, red, green, blue)
        self.red = red
        self.green = green
        self.blue = blue

    def __eq__(self, other, epsilon=0.00001):
        return fabs(self.red - other.red) < epsilon and \
            fabs(self.green - other.green) < epsilon and \
            fabs(self.blue - other.blue) < epsilon

    def __add__(self, other):
        added_tuple = super().__add__(other)
        return Colour(added_tuple.x, added_tuple.y, added_tuple.z)

    def __sub__(self, other):
        added_tuple = super().__sub__(other)
        return Colour(added_tuple.x, added_tuple.y, added_tuple.z)

    def __mul__(self, other):
        if type(other) is Colour:
            return Colour(self.red * other.red, self.green * other.green, self.blue * other.blue)
        else:
            added_tuple = super().__mul__(other)
            return Colour(added_tuple.x, added_tuple.y, added_tuple.z)

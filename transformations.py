from matrices import Matrix
from tuples import Vector


class Transformations:
    def __init__(self):
        pass

    @staticmethod
    def view_transform(from_point, to_point, up_vector):
        forward = Vector.from_tuple(to_point - from_point).normalise()
        up_norm = up_vector.normalise()
        left = forward.cross(up_norm)
        true_up = left.cross(forward)

        orientation = Matrix([[left.x, left.y, left.z, 0],
                              [true_up.x, true_up.y, true_up.z, 0],
                              [-forward.x, -forward.y, -forward.z, 0],
                              [0, 0, 0, 1]])

        return orientation * Matrix.translation(-from_point.x, -from_point.y, -from_point.z)

from math import tan
from matrices import Matrix
from tuples import *
from rays import Ray
from canvas import Canvas


class Camera:
    _transform = None
    _transform_inverse = None

    def __init__(self, horizontal_size, vertical_size, field_of_view):
        self.hsize = horizontal_size
        self.vsize = vertical_size
        self.field_of_view = field_of_view
        self.pixel_size = 0
        self.half_width = 0
        self.half_height = 0
        self._transform = Matrix.identity(4)
        self._transform_inverse = Matrix.identity(4)
        self.initialise()

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, value):
        self._transform = value
        self._transform_inverse = self.transform.inverse()

    def initialise(self):
        half_view = tan(self.field_of_view / 2)
        aspect = self.hsize / self.vsize
        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view
        self.pixel_size = self.half_width * 2 / self.hsize

    def ray_for_pixel(self, px, py):
        x_offset = (px + 0.5) * self.pixel_size
        y_offset = (py + 0.5) * self.pixel_size

        world_x = self.half_width - x_offset
        world_y = self.half_height - y_offset

        pixel = self._transform_inverse * Point(world_x, world_y, -1)
        origin = Point.from_tuple(self._transform_inverse * Point(0, 0, 0))
        direction = Vector.from_tuple(pixel - origin).normalise()

        return Ray(origin, direction)

    def render(self, world, reflect_depth=5, show_progress=False):
        image = Canvas(self.hsize, self.vsize)

        for y in range(self.vsize):
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                colour = world.colour_at(ray, reflect_depth)
                image.write_pixel(x, y, colour)
            if show_progress:
                print(f'{int(100 * y / self.vsize)}% complete')

        return image

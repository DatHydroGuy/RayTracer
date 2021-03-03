from PIL import Image
from colours import Colour


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('RGB', (width, height))

    def get_image_data(self, band=None):
        return [Colour(c[0], c[1], c[2]) for c in self.image.getdata(band)]

    def get_pixel(self, x, y):
        colour = self.image.getpixel((x, y))
        return Colour(colour[0] / 255, colour[1] / 255, colour[2] / 255)

    def write_pixel(self, x, y, colour):
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return
        red = min(max(int(round(colour.red * 255)), 0), 255)
        green = min(max(int(round(colour.green * 255)), 0), 255)
        blue = min(max(int(round(colour.blue * 255)), 0), 255)
        self.image.putpixel((x, y), (red, green, blue))

    def canvas_to_ppm(self, file_name):
        with open(file_name, 'w') as f:
            f.write('P3\n')
            f.write(f'{self.width} {self.height}\n')
            f.write('255\n')
            for y in range(self.height):
                line = ''
                for x in range(self.width):
                    colour = self.image.getpixel((x, y))
                    line += f'{colour[0]} {colour[1]} {colour[2]} '
                    if len(line) > 70:
                        space_index = line[:70][::-1].index(' ')
                        break_at = 70 - space_index - 1
                        test = line[:break_at]
                        f.write(test + '\n')
                        line = line[break_at + 1:]
                f.write(line[:-1] + '\n')

    def write_to_ppm(self, file_name):
        self.image.save(file_name, format='PPM')

import unittest
from colours import *
from canvas import Canvas
from pathlib import Path


class CanvasTestCase(unittest.TestCase):
    def tearDown(self):
        my_file = Path("test.ppm")
        if my_file.is_file():
            my_file.unlink()

    def test_creating_a_canvas(self):
        # Arrange
        expected = Colour(0, 0, 0)

        # Act
        c = Canvas(10, 20)

        # Assert
        self.assertEqual(c.width, 10)
        self.assertEqual(c.height, 20)
        self.assertTrue(all(pix == expected for pix in c.get_image_data()))

    def test_writing_pixel_to_a_canvas(self):
        # Arrange
        c = Canvas(10, 20)
        red = Colour(1, 0, 0)

        # Act
        c.write_pixel(2, 3, red)

        # Assert
        self.assertEqual(c.get_pixel(2, 3), red)

    def test_constructing_ppm_header(self):
        # Arrange
        c = Canvas(5, 3)
        expected = 'P3\n5 3\n255\n'

        # Act
        c.canvas_to_ppm('test.ppm')
        with open('test.ppm', 'r') as f:
            data = f.readlines()
        header = ''.join(data[:3])

        # Assert
        self.assertEqual(header, expected)

    def test_constructing_ppm_pixel_data(self):
        # Arrange
        c = Canvas(5, 3)
        c1 = Colour(1.5, 0, 0)
        c2 = Colour(0, 0.5, 0)
        c3 = Colour(-0.5, 0, 1)
        expected = """255 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 128 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 255
"""

        # Act
        c.write_pixel(0, 0, c1)
        c.write_pixel(2, 1, c2)
        c.write_pixel(4, 2, c3)
        c.canvas_to_ppm('test.ppm')
        with open('test.ppm', 'r') as f:
            data = f.readlines()
        pixels = ''.join(data[3:6])

        # Assert
        self.assertEqual(pixels, expected)

    def test_splitting_long_lines_in_ppm_files(self):
        # Arrange
        c = Canvas(10, 2)
        c1 = Colour(1, 0.8, 0.6)
        expected = """255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204
153 255 204 153 255 204 153 255 204 153 255 204 153
255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204
153 255 204 153 255 204 153 255 204 153 255 204 153
"""

        # Act
        for y in range(2):
            for x in range(10):
                c.write_pixel(x, y, c1)
        c.canvas_to_ppm('test.ppm')
        with open('test.ppm', 'r') as f:
            data = f.readlines()
        pixels = ''.join(data[3:])

        # Assert
        self.assertEqual(pixels, expected)

    def test_ppm_file_ends_with_a_newline_character(self):
        # Arrange
        c = Canvas(5, 3)
        expected = '\n'

        # Act
        c.canvas_to_ppm('test.ppm')
        with open('test.ppm', 'r') as f:
            data = f.readlines()
        last_char = data[-1][-1]

        # Assert
        self.assertEqual(last_char, expected)


if __name__ == '__main__':
    unittest.main()

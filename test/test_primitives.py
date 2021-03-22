import unittest
from rays import Ray
from primitives import *
from matrices import Matrix
from materials import Material
from math import sqrt, pi


class TestShape(Shape):
    def intersects(self, ray):
        return super(TestShape, self).intersects(ray)

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

    def normal_at(self, point):
        return super(TestShape, self).normal_at(point)

    def local_normal_at(self, point):
        return Vector.from_tuple(point - Point(0, 0, 0))


class PrimitiveTestCase(unittest.TestCase):
    def test_shape_is_created_at_the_origin(self):
        # Arrange
        expected = Point(0, 0, 0)

        # Act
        s = TestShape()

        # Assert
        self.assertEqual(s.origin, expected)

    def test_shape_has_a_default_transformation(self):
        # Arrange
        expected = Matrix.identity(4)

        # Act
        s = TestShape()

        # Assert
        self.assertEqual(s.transform, expected)

    def test_shape_can_be_assigned_a_transformation(self):
        # Arrange
        expected = Matrix.translation(2, 3, 4)
        s = TestShape()

        # Act
        s.set_transform(expected)

        # Assert
        self.assertEqual(s.transform, expected)

    def test_shape_has_a_default_material(self):
        # Arrange
        expected = Material()

        # Act
        s = TestShape()

        # Assert
        self.assertEqual(s.material, expected)

    def test_shape_can_be_assigned_a_material(self):
        # Arrange
        expected = Material()
        expected.ambient = 1
        s = TestShape()

        # Act
        s.material = expected

        # Assert
        self.assertEqual(s.material, expected)

    def test_intersecting_a_scaled_shape_with_a_ray(self):
        # Arrange
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = TestShape()

        # Act
        s.set_transform(Matrix.scaling(2, 2, 2))
        s.intersects(ray)

        # Assert
        self.assertEqual(s.saved_ray.origin, Point(0, 0, -2.5))
        self.assertEqual(s.saved_ray.direction, Vector(0, 0, 0.5))

    def test_intersecting_a_translated_shape_with_a_ray(self):
        # Arrange
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = TestShape()

        # Act
        s.set_transform(Matrix.translation(5, 0, 0))
        s.intersects(ray)

        # Assert
        self.assertEqual(s.saved_ray.origin, Point(-5, 0, -5))
        self.assertEqual(s.saved_ray.direction, Vector(0, 0, 1))

    def test_normal_computation_on_a_translated_shape(self):
        # Arrange
        s = TestShape()
        s.set_transform(Matrix.translation(0, 1, 0))
        expected = Vector(0, 0.70711, -0.70711)

        # Act
        n = s.normal_at(Point(0, 1.70711, -0.70711))

        # Assert
        self.assertEqual(n, expected)

    def test_normal_computation_on_a_transformed_shape(self):
        # Arrange
        s = TestShape()
        m = Matrix.scaling(1, 0.5, 1) * Matrix.rotation_z(pi / 5)
        s.set_transform(m)
        expected = Vector(0, 0.97014, -0.24254)

        # Act
        n = s.normal_at(Point(0, sqrt(2) / 2, -sqrt(2) / 2))

        # Assert
        self.assertEqual(n, expected)


class SphereTestCase(unittest.TestCase):
    def test_sphere_is_a_shape(self):
        # Arrange

        # Act
        s = Sphere()

        # Assert
        self.assertIsInstance(s, Shape)

    def test_sphere_is_created_at_the_origin(self):
        # Arrange
        expected = Point(0, 0, 0)

        # Act
        s = Sphere()

        # Assert
        self.assertEqual(s.origin, expected)

    def test_spheres_are_created_with_unique_ids(self):
        # Arrange

        # Act
        s1 = Sphere()
        s2 = Sphere()

        # Assert
        self.assertNotEqual(s1.id, s2.id)

    def test_sphere_is_created_from_point_at_the_origin(self):
        # Arrange
        expected = Point(0, 0, 0)
        p = Point(0, 0, 0)

        # Act
        s = Sphere.from_point(p)

        # Assert
        self.assertEqual(s.origin, expected)

    def test_spheres_are_created_from_points_with_unique_ids(self):
        # Arrange
        p = Point(0, 0, 0)

        # Act
        s1 = Sphere.from_point(p)
        s2 = Sphere.from_point(p)

        # Assert
        self.assertNotEqual(s1.id, s2.id)

    def test_a_ray_through_a_sphere_intersects_the_sphere_at_two_points(self):
        # Arrange
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        expected1 = 4.0
        expected2 = 6.0

        # Act
        results = s.intersects(r)

        # Assert
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].t, expected1)
        self.assertEqual(results[1].t, expected2)

    def test_a_ray_tangent_to_a_sphere_intersects_at_one_unique_point(self):
        # Arrange
        r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
        s = Sphere()
        # NOTE: we will return a unique point, but TWICE!!!
        expected1 = 5.0
        expected2 = 5.0

        # Act
        results = s.intersects(r)

        # Assert
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].t, expected1)
        self.assertEqual(results[1].t, expected2)

    def test_a_ray_misses_a_sphere(self):
        # Arrange
        r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
        s = Sphere()

        # Act
        results = s.intersects(r)

        # Assert
        self.assertEqual(len(results), 0)

    def test_a_ray_originating_inside_a_sphere_intersects_the_sphere_at_two_points(self):
        # Arrange
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        s = Sphere()
        expected1 = -1.0
        expected2 = 1.0

        # Act
        results = s.intersects(r)

        # Assert
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].t, expected1)
        self.assertEqual(results[1].t, expected2)

    def test_a_ray_going_away_from_a_sphere_intersects_the_sphere_at_two_points(self):
        # Arrange
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        s = Sphere()
        expected1 = -6.0
        expected2 = -4.0

        # Act
        results = s.intersects(r)

        # Assert
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].t, expected1)
        self.assertEqual(results[1].t, expected2)

    def test_intersect_sets_the_object_on_the_intersection(self):
        # Arrange
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()

        # Act
        results = s.intersects(r)

        # Assert
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].object, s)
        self.assertEqual(results[1].object, s)

    def test_changing_the_transform_of_a_sphere(self):
        # Arrange
        s = Sphere()
        translation = Matrix.translation(2, 3, 4)

        # Act
        s.set_transform(translation)

        # Assert
        self.assertEqual(s.transform, translation)

    def test_intersecting_a_scaled_sphere_with_a_ray(self):
        # Arrange
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()

        # Act
        s.set_transform(Matrix.scaling(2, 2, 2))
        xs = s.intersects(r)

        # Assert
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 3)
        self.assertEqual(xs[1].t, 7)

    def test_intersecting_a_translated_sphere_with_a_ray(self):
        # Arrange
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()

        # Act
        s.set_transform(Matrix.translation(5, 0, 0))
        xs = s.intersects(r)

        # Assert
        self.assertEqual(len(xs), 0)

    def test_normal_to_surface_of_a_sphere_at_point_on_x_axis(self):
        # Arrange
        pt = Point(1, 0, 0)
        s = Sphere()
        expected = Vector(1, 0, 0)

        # Act
        n = s.normal_at(pt)

        # Assert
        self.assertEqual(n, expected)

    def test_normal_to_surface_of_a_sphere_at_point_on_y_axis(self):
        # Arrange
        pt = Point(0, 1, 0)
        s = Sphere()
        expected = Vector(0, 1, 0)

        # Act
        n = s.normal_at(pt)

        # Assert
        self.assertEqual(n, expected)

    def test_normal_to_surface_of_a_sphere_at_point_on_z_axis(self):
        # Arrange
        pt = Point(0, 0, 1)
        s = Sphere()
        expected = Vector(0, 0, 1)

        # Act
        n = s.normal_at(pt)

        # Assert
        self.assertEqual(n, expected)

    def test_normal_to_surface_of_a_sphere_at_a_nonaxial_point(self):
        # Arrange
        pt = Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)
        s = Sphere()
        expected = Vector(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)

        # Act
        n = s.normal_at(pt)

        # Assert
        self.assertEqual(n, expected)

    def test_normal_is_a_normalised_vector(self):
        # Arrange
        pt = Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)
        s = Sphere()

        # Act
        n = s.normal_at(pt)

        # Assert
        self.assertEqual(n, n.normalise())


class PlaneTestCase(unittest.TestCase):
    def test_normal_of_a_plane_is_constant_everywhere(self):
        # Arrange
        p = Plane()
        expected = Vector(0, 1, 0)

        # Act
        n1 = p.local_normal_at(Point(0, 0, 0))
        n2 = p.local_normal_at(Point(10, 0, -10))
        n3 = p.local_normal_at(Point(-5, 0, 150))

        # Assert
        self.assertEqual(n1, expected)
        self.assertEqual(n2, expected)
        self.assertEqual(n3, expected)

    def test_intersect_with_a_ray_parallel_to_the_plane(self):
        # Arrange
        p = Plane()
        r = Ray(Point(0, 10, 0), Vector(0, 0, 1))

        # Act
        xs = p.local_intersect(r)

        # Assert
        self.assertEqual(len(xs), 0)

    def test_intersect_with_a_coplanar_ray(self):
        # Arrange
        p = Plane()
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))

        # Act
        xs = p.local_intersect(r)

        # Assert
        self.assertEqual(len(xs), 0)

    def test_intersecting_a_plane_from_above(self):
        # Arrange
        p = Plane()
        r = Ray(Point(0, 1, 0), Vector(0, -1, 0))

        # Act
        xs = p.local_intersect(r)

        # Assert
        self.assertEqual(len(xs), 1)
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[0].object, p)

    def test_intersecting_a_plane_from_below(self):
        # Arrange
        p = Plane()
        r = Ray(Point(0, -1, 0), Vector(0, 1, 0))

        # Act
        xs = p.local_intersect(r)

        # Assert
        self.assertEqual(len(xs), 1)
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[0].object, p)

    def test_the_glass_sphere_helper_function(self):
        # Arrange
        s = Sphere.glass_sphere()

        # Act

        # Assert
        self.assertEqual(s.transform, Matrix.identity(4))
        self.assertEqual(s.material.transparency, 1)
        self.assertEqual(s.material.refractive_index, 1.5)


class CubeTestCase(unittest.TestCase):
    def test_a_ray_intersects_a_cube(self):
        # Arrange
        origins = [Point(5, 0.5, 0), Point(-5, 0.5, 0), Point(0.5, 5, 0), Point(0.5, -5, 0),
                   Point(0.5, 0, 5), Point(0.5, 0, -5), Point(0, 0.5, 0)]
        directions = [Vector(-1, 0, 0), Vector(1, 0, 0), Vector(0, -1, 0), Vector(0, 1, 0),
                      Vector(0, 0, -1), Vector(0, 0, 1), Vector(0, 0, 1)]
        expected_t1s = [4, 4, 4, 4, 4, 4, -1]
        expected_t2s = [6, 6, 6, 6, 6, 6, 1]
        c = Cube()

        for idx, origin in enumerate(origins):
            with self.subTest(origin=origin):
                direction = directions[idx]
                expected_t1 = expected_t1s[idx]
                expected_t2 = expected_t2s[idx]
                r = Ray(origin, direction)

                # Act
                xs = c.local_intersect(r)

                # Assert
                self.assertEqual(xs[0].t, expected_t1)
                self.assertEqual(xs[1].t, expected_t2)

    def test_a_ray_misses_a_cube(self):
        # Arrange
        origins = [Point(-2, 0, 0), Point(0, -2, 0), Point(0, 0, -2),
                   Point(2, 0, 2), Point(0, 2, 2), Point(2, 2, 0)]
        directions = [Vector(0.2673, 0.5345, 0.8018), Vector(0.8018, 0.2673, 0.5345), Vector(0.5345, 0.8018, 0.2673),
                      Vector(0, 0, -1), Vector(0, -1, 0), Vector(-1, 0, 0)]
        c = Cube()

        for idx, origin in enumerate(origins):
            with self.subTest(origin=origin):
                direction = directions[idx]
                r = Ray(origin, direction)

                # Act
                xs = c.local_intersect(r)

                # Assert
                self.assertEqual(len(xs), 0)

    def test_the_normal_on_the_surface_of_a_cube(self):
        # Arrange
        points = [Point(1, 0.5, -0.8), Point(-1, -0.2, 0.9), Point(-0.4, 1, -0.1), Point(0.3, -1, -0.7),
                  Point(-0.6, 0.3, 1), Point(0.4, 0.4, -1), Point(1, 1, 1), Point(-1, -1, -1)]
        vectors = [Vector(1, 0, 0), Vector(-1, 0, 0), Vector(0, 1, 0), Vector(0, -1, 0), Vector(0, 0, 1),
                   Vector(0, 0, -1), Vector(1, 0, 0), Vector(-1, 0, 0)]
        c = Cube()

        for idx, point in enumerate(points):
            with self.subTest(point=point):

                # Act
                normal = c.local_normal_at(point)

                # Assert
                self.assertEqual(normal, vectors[idx])


class CylinderTestCase(unittest.TestCase):
    def test_a_ray_misses_a_cylinder(self):
        # Arrange
        origins = [Point(1, 0, 0), Point(0, 0, 0), Point(0, 0, -5)]
        directions = [Vector(0, 1, 0), Vector(0, 1, 0), Vector(1, 1, 1)]
        c = Cylinder()

        for idx, origin in enumerate(origins):
            with self.subTest(origin=origin):
                direction = directions[idx].normalise()
                r = Ray(origin, direction)

                # Act
                xs = c.local_intersect(r)

                # Assert
                self.assertEqual(len(xs), 0)

    def test_a_ray_intersects_a_cylinder(self):
        # Arrange
        origins = [Point(1, 0, -5), Point(0, 0, -5), Point(0.5, 0, -5)]
        directions = [Vector(0, 0, 1), Vector(0, 0, 1), Vector(0.1, 1, 1)]
        expected_t1s = [5, 4, 6.80798]
        expected_t2s = [5, 6, 7.08872]
        c = Cylinder()

        for idx, origin in enumerate(origins):
            with self.subTest(origin=origin):
                direction = directions[idx].normalise()
                expected_t1 = expected_t1s[idx]
                expected_t2 = expected_t2s[idx]
                r = Ray(origin, direction)

                # Act
                xs = c.local_intersect(r)

                # Assert
                self.assertAlmostEqual(xs[0].t, expected_t1, 5)
                self.assertAlmostEqual(xs[1].t, expected_t2, 5)

    def test_the_normal_on_the_surface_of_a_cylinder(self):
        # Arrange
        points = [Point(1, 0, 0), Point(0, 5, -1), Point(0, -2, 1), Point(-1, 1, 0)]
        vectors = [Vector(1, 0, 0), Vector(0, 0, -1), Vector(0, 0, 1), Vector(-1, 0, 0)]
        c = Cylinder()

        for idx, point in enumerate(points):
            with self.subTest(point=point):

                # Act
                normal = c.local_normal_at(point)

                # Assert
                self.assertEqual(normal, vectors[idx])

    def test_the_default_minimum_and_maximum_extents_of_a_cylinder(self):
        # Arrange
        c = Cylinder()

        # Act

        # Assert
        self.assertEqual(c.minimum, -float('inf'))
        self.assertEqual(c.maximum, float('inf'))

    def test_intersecting_a_constrained_cylinder(self):
        # Arrange
        origins = [Point(0, 1.5, 0), Point(0, 3, -5), Point(0, 0, -5),
                   Point(0, 2, -5), Point(0, 1, -5), Point(0, 1.5, -2)]
        directions = [Vector(0.1, 1, 0), Vector(0, 0, 1), Vector(0, 0, 1),
                      Vector(0, 0, 1), Vector(0, 0, 1), Vector(0, 0, 1)]
        expected_counts = [0, 0, 0, 0, 0, 2]
        c = Cylinder()
        c.minimum = 1
        c.maximum = 2

        for idx, origin in enumerate(origins):
            with self.subTest(origin=origin):
                direction = directions[idx].normalise()
                expected_count = expected_counts[idx]
                r = Ray(origin, direction)

                # Act
                xs = c.local_intersect(r)

                # Assert
                self.assertEqual(len(xs), expected_count)

    def test_the_default_closed_value_of_a_cylinder(self):
        # Arrange
        c = Cylinder()

        # Act

        # Assert
        self.assertFalse(c.closed)

    def test_intersecting_the_end_caps_of_a_closed_cylinder(self):
        # Arrange
        origins = [Point(0, 3, 0), Point(0, 3, -2), Point(0, 4, -2), Point(0, 0, -2), Point(0, -1, -2)]
        directions = [Vector(0, -1, 0), Vector(0, -1, 2), Vector(0, -1, 1), Vector(0, 1, 2), Vector(0, 1, 1)]
        expected_counts = [2, 2, 2, 2, 2]
        c = Cylinder()
        c.minimum = 1
        c.maximum = 2
        c.closed = True

        for idx, origin in enumerate(origins):
            with self.subTest(origin=origin):
                direction = directions[idx].normalise()
                expected_count = expected_counts[idx]
                r = Ray(origin, direction)

                # Act
                xs = c.local_intersect(r)

                # Assert
                self.assertEqual(len(xs), expected_count)

    def test_normal_vectors_on_the_end_caps_of_a_closed_cylinder(self):
        # Arrange
        points = [Point(0, 1, 0), Point(0.5, 1, 0), Point(0, 1, 0.5),
                  Point(0, 2, 0), Point(0.5, 2, 0), Point(0, 2, 0.5)]
        normals = [Vector(0, -1, 0), Vector(0, -1, 0), Vector(0, -1, 0),
                   Vector(0, 1, 0), Vector(0, 1, 0), Vector(0, 1, 0)]
        c = Cylinder()
        c.minimum = 1
        c.maximum = 2
        c.closed = True

        for idx, point in enumerate(points):
            with self.subTest(point=point):
                expected_normal = normals[idx]

                # Act
                n = c.local_normal_at(point)

                # Assert
                self.assertEqual(n, expected_normal)


class ConeTestCase(unittest.TestCase):
    def test_a_ray_intersects_a_cone(self):
        # Arrange
        origins = [Point(0, 0, -5), Point(0, 0, -5), Point(1, 1, -5)]
        directions = [Vector(0, 0, 1), Vector(1, 1, 1), Vector(-0.5, -1, 1)]
        expected_t1s = [5, 8.66025, 4.55006]
        expected_t2s = [5, 8.66025, 49.44994]
        c = Cone()

        for idx, origin in enumerate(origins):
            with self.subTest(origin=origin):
                direction = directions[idx].normalise()
                expected_t1 = expected_t1s[idx]
                expected_t2 = expected_t2s[idx]
                r = Ray(origin, direction)

                # Act
                xs = c.local_intersect(r)

                # Assert
                self.assertAlmostEqual(xs[0].t, expected_t1, 5)
                self.assertAlmostEqual(xs[1].t, expected_t2, 5)

    def test_a_ray_parallel_to_one_conical_half_intersects_the_other_cone_only_once(self):
        # Arrange
        c = Cone()
        direction = Vector(0, 1, 1).normalise()
        expected = 0.35355
        r = Ray(Point(0, 0, -1), direction)

        # Act
        xs = c.local_intersect(r)

        # Assert
        self.assertEqual(len(xs), 1)
        self.assertAlmostEqual(xs[0].t, expected, 5)

    def test_intersecting_a_constrained_cones_end_caps(self):
        # Arrange
        origins = [Point(0, 0, -5), Point(0, 0, -0.25), Point(0, 0, -0.25)]
        directions = [Vector(0, 1, 0), Vector(0, 1, 1), Vector(0, 1, 0)]
        expected_counts = [0, 2, 4]
        c = Cone()
        c.minimum = -0.5
        c.maximum = 0.5
        c.closed = True

        for idx, origin in enumerate(origins):
            with self.subTest(origin=origin):
                direction = directions[idx].normalise()
                expected_count = expected_counts[idx]
                r = Ray(origin, direction)

                # Act
                xs = c.local_intersect(r)

                # Assert
                self.assertEqual(len(xs), expected_count)

    def test_normal_vectors_on_a_closed_cone(self):
        # Arrange
        points = [Point(0, 0, 0), Point(1, 1, 1), Point(-1, -1, 0)]
        normals = [Vector(0, 0, 0), Vector(1, -sqrt(2), 1), Vector(-1, 1, 0)]
        c = Cone()
        c.minimum = -0.5
        c.maximum = 0.5
        c.closed = True

        for idx, point in enumerate(points):
            with self.subTest(point=point):
                expected_normal = normals[idx]

                # Act
                n = c.local_normal_at(point)

                # Assert
                self.assertEqual(n, expected_normal)


if __name__ == '__main__':
    unittest.main()

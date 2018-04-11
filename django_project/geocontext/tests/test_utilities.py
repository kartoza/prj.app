# coding=utf-8
"""Test for utilities module."""

import os

from django.test import SimpleTestCase
from geocontext.utilities import (
    convert_coordinate, parse_gml_geometry, convert_2d_to_3d)
from django.contrib.gis.geos import (
    Point, LineString, LinearRing, Polygon, MultiPoint,
    MultiLineString, MultiPolygon)

test_data_directory = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'data')


class TestUtilities(SimpleTestCase):
    """Test for utilities module."""

    def test_convert_coordinate(self):
        """Test convert_coordinate method."""
        result = convert_coordinate(1, 1, 4326, 3857)
        self.assertAlmostEqual(result[0], 111319.49, places=2)
        self.assertAlmostEqual(result[1], 111325.14, places=2)

    def test_parse_geometry_gml(self):
        """Test parse_gml_geometry"""
        gml_file_path = os.path.join(test_data_directory, 'wfs.xml')
        self.assertTrue(os.path.exists(gml_file_path))
        with open(gml_file_path) as file:
            gml_string = file.read()
        geom = parse_gml_geometry(gml_string)
        self.assertIsNotNone(geom)
        self.assertTrue(geom.valid)
        self.assertEqual(geom.geom_type, 'Polygon')

    def test_convert_2d_to_3d(self):
        """Test convert_2d_to_3d."""
        point = Point(1, 1, srid=4326)
        line_string = LineString((0, 0), (1, 1), srid=4326)
        line_string_2 = LineString((2, 2), (3, 3), srid=4326)
        linear_ring = LinearRing((0, 0), (0, 1), (1, 1), (0, 0), srid=4326)
        ext_coords = ((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
        int_coords = (
            (0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4))
        polygon = Polygon(ext_coords, int_coords, srid=4326)
        polygon_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)), srid=4326)
        multi_point = MultiPoint(Point(0, 0), Point(1, 1), srid=4326)
        multi_line_string = MultiLineString(
            line_string, line_string_2, srid=4326)
        multi_polygon = MultiPolygon(polygon, polygon_2, srid=4326)

        geometries_2d = [
            point,
            line_string,
            linear_ring,
            polygon,
            multi_point,
            multi_line_string,
            multi_polygon
        ]

        for geometry_2d in geometries_2d:
            print('Checking for %s' % geometry_2d.geom_type)
            geometry_3d = convert_2d_to_3d(geometry_2d)
            self.assertTrue(geometry_3d.hasz)
            self.assertEqual(geometry_3d.srid, geometry_2d.srid)
            self.assertEqual(geometry_3d.geom_type, geometry_2d.geom_type)
            if geometry_3d.geom_type == 'Point':
                self.assertEqual(geometry_3d.z, 0)
            elif geometry_3d.geom_type == 'MultiPoint':
                zs = [p.z for p in geometry_3d]
                self.assertEqual(sum(zs), 0)
            elif geometry_3d.geom_type in ['MultiLineString', 'Polygon']:
                zs = [sum(ls.z) for ls in geometry_3d]
                self.assertEqual(sum(zs), 0)
            elif geometry_3d.geom_type == 'MultiPolygon':
                zs = [sum([sum(ls.z) for ls in poly]) for poly in geometry_3d]
                self.assertEqual(sum(zs), 0)
            elif geometry_3d.geom_type in ['LineString', 'LinearRing']:
                self.assertEqual(sum(geometry_3d.z), 0)

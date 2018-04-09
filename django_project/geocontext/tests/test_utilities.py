# coding=utf-8
"""Test for utilities module."""

import os

from django.test import SimpleTestCase
from geocontext.utilities import convert_coordinate, parse_gml_geometry

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

# coding=utf-8
"""Test for utilities module."""

from django.test import SimpleTestCase
from geocontext.utilities import convert_coordinate


class TestUtilities(SimpleTestCase):
    """Test for utilities module."""

    def test_convert_coordinate(self):
        """Test convert_coordinate method."""
        result = convert_coordinate(1, 1, 4326, 3857)
        self.assertAlmostEqual(result[0], 111319.49, places=2)
        self.assertAlmostEqual(result[1], 111325.14, places=2)

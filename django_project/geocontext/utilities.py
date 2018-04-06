# coding=utf-8
"""Utilities module for geocontext app."""

from django.contrib.gis.geos import Point


def convert_coordinate(x, y, epsg_source, epsg_target):
    """Convert coordinate x y from crs_source to crs_target.

    :param x: The value of x coordinate.
    :type x: float

    :param y: The value of y coordinate.
    :type y: float

    :param epsg_source: The source EPSG coordinate reference.
    :type epsg_source: int

    :param epsg_target: The target EPSG coordinate reference.
    :type epsg_target: int

    :return: tuple of converted x and y in float.
    :rtype: tuple(float, float)
    """

    # create a geometry from coordinates
    point = Point(x, y, srid=epsg_source)

    point.transform(epsg_target)

    return point.x, point.y

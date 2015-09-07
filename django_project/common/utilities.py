# coding=utf-8
"""**Utilities functions**
"""

__author__ = 'Ismail Sunni <ismail@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '23/04/2014'
__license__ = ''
__copyright__ = ''


from slugify import Slugify

version_slugify = Slugify()
version_slugify.safe_chars = '.'

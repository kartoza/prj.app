# noinspection PyUnresolvedReferences,PyPackageRequirements
import factory
import random
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from base.models import LocationType, LocationSite, Profile


class LocationTypeF(factory.django.DjangoModelFactory):
    """
    Location type factory
    """

    class Meta:
        model = LocationType

    name = factory.Sequence(lambda n: 'Test location type %s' % n)
    description = u'Only for testing'
    allowed_geometry = 'POINT'


class LocationSiteF(factory.django.DjangoModelFactory):
    """
    Location site factory
    """

    class Meta:
        model = LocationSite

    location_type = factory.SubFactory(LocationTypeF)
    geometry_point = Point(
        random.uniform(-180.0, 180.0),
        random.uniform(-90.0, 90.0)
    )


class ProfileF(factory.django.DjangoModelFactory):
    """
    Profile site factory
    """

    class Meta:
        model = Profile

    user = factory.SubFactory(User)
    qualifications = factory.Sequence(lambda n: "qualifications%s" % n)
    other = factory.Sequence(lambda n: "other%s" % n)

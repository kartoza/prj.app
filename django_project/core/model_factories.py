# noinspection PyUnresolvedReferences,PyPackageRequirements
import factory
import datetime

from django.conf import settings
from django import VERSION as DJANGO_VERSION
from django.contrib.auth.models import User
from djstripe.models import Customer

if DJANGO_VERSION[:2] >= (1, 4):
    from django.utils import timezone


class CustomerF(factory.django.DjangoModelFactory):

    class Meta:
        model = Customer

    name = factory.Sequence(lambda n: "name%s" % n)
    balance = factory.Sequence(lambda n: n)
    delinquent = False


# noinspection PyProtectedMember
class UserF(factory.django.DjangoModelFactory):

    class Meta:
        model = User
    # @classmethod
    # def _setup_next_sequence(cls):
    #     try:
    #         return cls._associated_class.objects.values_list(
    #             'id', flat=True).order_by('-id')[0] + 1
    #     except IndexError:
    #         return 0

    username = factory.Sequence(lambda n: "username%s" % n)
    first_name = factory.Sequence(lambda n: "first_name%s" % n)
    last_name = factory.Sequence(lambda n: "last_name%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    password = ''
    is_staff = False
    is_active = True
    is_superuser = False
    if DJANGO_VERSION[:2] >= (1, 4) and settings.USE_TZ:
        last_login = timezone.datetime(2000, 1, 1).replace(tzinfo=timezone.utc)
        date_joined = timezone.datetime(1999, 1, 1).replace(
            tzinfo=timezone.utc)
    else:
        last_login = datetime.datetime(2000, 1, 1)
        date_joined = datetime.datetime(1999, 1, 1)

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserF, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

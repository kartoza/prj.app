# noinspection PyUnresolvedReferences,PyPackageRequirements
import factory
from django.utils import timezone

from fish.models import (
    FishCollectionRecord,
    IUCNStatus,
    Taxon,
)
from base.tests.model_factories import LocationSiteF
from core.tests.model_factories import UserF


class IUCNStatusF(factory.django.DjangoModelFactory):
    """
    Iucn status factory
    """
    class Meta:
        model = IUCNStatus

    name = factory.Sequence(lambda n: u'Test name %s' % n)
    sensitive = False


class TaxonF(factory.django.DjangoModelFactory):
    """
    Taxon factory
    """
    class Meta:
        model = Taxon

    iucn_status = factory.SubFactory(IUCNStatusF)
    common_name = factory.Sequence(lambda n: u'Test common name %s' % n)
    scientific_name = factory.Sequence(
            lambda n: u'Test scientific name %s' % n)
    author = factory.Sequence(lambda n: u'Test author %s' % n)


class FishCollectionRecordF(factory.django.DjangoModelFactory):
    """
    Fish collection record factory
    """
    class Meta:
        model = FishCollectionRecord

    site = factory.SubFactory(LocationSiteF)
    original_species_name = factory.Sequence(
            lambda n: u'Test original species name %s' % n)
    habitat = 'euryhaline'
    category = 'alien'
    present = True
    collection_date = timezone.now()
    collector = factory.Sequence(
            lambda n: u'Test collector %s' % n)
    owner = factory.SubFactory(UserF)
    notes = factory.Sequence(
            lambda n: u'Test notes %s' % n)
    taxon_gbif_id = factory.SubFactory(TaxonF)

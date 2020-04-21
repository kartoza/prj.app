# coding=utf-8
"""Command to set the value of the Status of the Certifying Organisation.
This command also creates Status Approved, In Progress and Rejected,
if those status aren't created on the database yet.

"""

from django.core.management.base import BaseCommand
from ...models.certifying_organisation import CertifyingOrganisation
from ...models.status import Status


class Command(BaseCommand):
    """Set the status of the existing certifying organisations and creates
    Status objects for Pending, Approved and Rejected.

    """

    help = 'Set the status of the existing certifying ' \
           'organisations and creates. Status objects for Pending, ' \
           'Approved and Rejected.'

    def handle(self, *args, **options):
        print('Begin process....')
        certifying_organisations = \
            CertifyingOrganisation.objects.filter(status=None)

        print(
            'Begin process to set existing pending certifying organisations.'
        )
        # Set status for pending certifying organisations
        pending_certifying_organisation = certifying_organisations.filter(
            approved=False
        )
        for organisation in pending_certifying_organisation:
            pending_status, created = Status.objects.get_or_create(
                name='Pending',
                project=organisation.project
            )
            organisation.status = pending_status
            organisation.save()
        print(
            'Status of all existing pending certifying '
            'organisations has been set to Pending'
        )
        print('------------------------------------------------------------')
        print(
            'Begin process to set existing approved certifying organisations.'
        )

        # Set status for approved certifying organisations
        approved_certifying_organisation = certifying_organisations.filter(
            approved=True
        )
        for organisation in approved_certifying_organisation:
            approved_status, created = Status.objects.get_or_create(
                name='Approved',
                project=organisation.project
            )
            organisation.status = approved_status
            organisation.save()

        print(
            'Status of all existing approved certifying '
            'organisations has been set to Approved'
        )
        print('------------------------------------------------------------')
        print(
            'Begin process to set existing rejected certifying organisations.'
        )

        # Set status for rejected certifying organisations
        rejected_certifying_organisation = certifying_organisations.filter(
            rejected=True
        )
        for organisation in rejected_certifying_organisation:
            rejected_status, created = Status.objects.get_or_create(
                name='Rejected',
                project=organisation.project
            )
            organisation.status = rejected_status
            organisation.save()
        print(
            'Status of all existing approved certifying '
            'organisations has been set to Rejected'
        )
        print('------------------------------------------------------------')
        print('')
        print('Process finished.')

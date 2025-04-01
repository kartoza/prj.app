from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from ...models.certifying_organisation import CertifyingOrganisation
from ...models.status import Status
from ...views import send_rejection_email


class Command(BaseCommand):
    """Reject pending certifying organisations
    that were created more than one year ago
    and set their status to Rejected.

    """

    help = 'Reject pending certifying organisations\
          that were created more than one year ago \
            and set their status to Rejected.'

    def add_arguments(self, parser):
        # Adding a custom argument for the number of days
        parser.add_argument(
            '--days',
            type=int,
            default=356,
            help='Number of days from now to filter records for update.'
        )

    def handle(self, *args, **options):
        print('Begin process....')
        days = options.get('days')
        print(f'Number of days: {days}')
        one_year_ago = timezone.now() - timedelta(days=days)
        old_organisations = CertifyingOrganisation.unapproved_objects.all()

        print('Begin process to reject old certifying organisations.')

        count = 0
        for organisation in old_organisations:
            if organisation.creation_date < one_year_ago:
                rejected_status, created = Status.objects.get_or_create(
                    name='Rejected',
                    project=organisation.project
                )
                organisation.status = rejected_status
                organisation.rejected = True
                organisation.save()

                send_rejection_email(
                    organisation,
                    'changelog.qgis.org',
                    'https'
                )
                count += 1
                print(f'{organisation.name} has been set to Rejected')
        print(f'{count} certifying organisations has been set to Rejected')
        print('------------------------------------------------------------')
        print('Process finished.')

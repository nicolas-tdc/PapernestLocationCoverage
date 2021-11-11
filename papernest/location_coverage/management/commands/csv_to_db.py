"""Manage.py command to import coverage data from CSV to DB."""


from django.core.management.base import BaseCommand, CommandError
from location_coverage.models import Provider, CoverageSite, CoverageType


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        Add optional argument to delete existing DB entries.
        :param parser:
        :return: void
        """
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Replace current providers, coverage sites and types',
        )

    def handle(self, *args, **options):
        """
        Handle the command execution to import data from CSV to DB
        :param args:
        :param options:
        :return: Command success or failure message
        """
        check_duplicates = False

        if options['delete']:
            Provider.objects.all().delete()
            CoverageSite.objects.all().delete()
            CoverageType.objects.all().delete()
        else:
            check_duplicates = True

        # Import CSV to DB / Create helpers file

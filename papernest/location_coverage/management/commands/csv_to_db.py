"""Manage.py command to import coverage data from CSV to DB."""


from django.core.management.base import BaseCommand, CommandError
from ._helpers import CsvToDbHelpers
from location_coverage.models import Provider, CoverageSite, CoverageType


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        Add optional argument to delete existing database entries.
        :param parser:
        :return: void
        """
        parser.add_argument(
            '--reset_all_coverage',
            action='store_true',
            help='Remove all coverage entries from database',
        )
        parser.add_argument(
            '--reset_coverage_sites',
            action='store_true',
            help='Remove all coverage sites from database',
        )

    def handle(self, *args, **options):
        """
        Handle the command execution to import data from CSV to DB
        :param args:
        :param options:
        :return: Command success or failure message
        """
        if options['reset_all_coverage']:
            CoverageSite.objects.all().delete()
            CoverageType.objects.all().delete()
            Provider.objects.all().delete()
        elif options['reset_coverage_sites']:
            CoverageSite.objects.all().delete()

        csv_url = (
            'https://www.data.gouv.fr/s/resources/monreseaumobile/20180228-174515/'
            '2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv'
        )
        providers_data = {
            '20801': {'name': 'Orange', 'country': 'FR'},
            '20810': {'name': 'SFR', 'country': 'FR'},
            '20815': {'name': 'Free', 'country': 'FR'},
            '20820': {'name': 'Bouygue', 'country': 'FR'},
        }
        csv_model_mapping = {
            'Operateur': 'Provider__code',
            'X': 'CoverageSite__x',
            'Y': 'CoverageSite__y',
            '2G': 'CoverageType__2G',
            '3G': 'CoverageType__3G',
            '4G': 'CoverageType__4G',
        }
        helpers = CsvToDbHelpers(csv_url, providers_data, csv_model_mapping, ';')
        instantiation_msg = helpers.instantiate_models_from_reader()
        self.stdout.write(self.style.SUCCESS(instantiation_msg))

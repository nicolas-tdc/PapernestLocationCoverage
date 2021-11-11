"""Manage.py command to import coverage data from CSV to DB."""


from django.core.management.base import BaseCommand, CommandError
from ._helpers import CsvToDbHelpers
from location_coverage.models import Provider, CoverageSite, CoverageType


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        Add optional argument to delete coverage sites database entries.
        :param parser:
        :return: void
        """
        parser.add_argument(
            '--replace_sites',
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
        csv_url = 'https://www.data.gouv.fr/s/resources/monreseaumobile/20180228-174515/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv'
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
        helpers = CsvToDbHelpers(csv_url, providers_data, csv_model_mapping)

        if options['replace_sites']:
            CoverageSite.objects.all().delete()

        # TODO Command Error
        helpers.instantiate_models_from_reader()

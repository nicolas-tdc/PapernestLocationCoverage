"""Tests for CSV to database import."""


from django.test import TestCase

from location_coverage.management.commands._helpers import CsvToDbHelpers
from location_coverage.models import Provider, CoverageSite, CoverageType


class CSVToDbTest(TestCase):
    """
    Tests for CSV to DB command line import.
    """
    def setUp(self):
        """
        Set up CSV to DB helpers for testing.
        """
        csv_model_mapping = {
            'Operateur': 'Provider__code',
            'X': 'CoverageSite__x',
            '2G': 'CoverageType__2G',
        }
        providers_data = {'20801': {'name': 'Orange', 'country': 'FR'}}
        self.helpers = CsvToDbHelpers('', providers_data, csv_model_mapping, ';')

    def test_map_column_to_fields(self):
        """
        Tests mapping of csv columns to model fields.
        """
        row = {
            'Operateur': '20801',
            'X': '102980',
            '2G': '1',
        }
        mapped_fields = self.helpers.map_columns_to_fields(row)

        expected = {
            'Provider__code': '20801',
            'CoverageSite__x': '102980',
            'CoverageType__2G': '1',
        }
        self.assertEqual(mapped_fields, expected)

    def test_lambert93_to_gps(self):
        """
        Tests conversion of lambert93 coordinates to latitude and longitude.
        """
        lambert93_coordinates = [
            {'X': '102980', 'Y': '6847973', 'expected': (-5.0888561153013425, 48.456574558829914)},
            {'X': '103113', 'Y': '6848661', 'expected': (-5.088018169414727, 48.46285384829354)},
            {'X': '103114', 'Y': '6848664', 'expected': (-5.088008862939317, 48.462881615228916)},
        ]
        for coordinates in lambert93_coordinates:
            result = self.helpers.lambert93_to_gps(coordinates['X'], coordinates['Y'])
            self.assertEqual(result, coordinates['expected'])

    def test_csv_data_formatter(self):
        """
        Tests csv data formatting.
        """
        reader = [
            {
                'Operateur': '20801',
                'X': '102980',
                '2G': '1',
            },
        ]
        result = self.helpers.csv_data_formatter(reader)
        expected = {
            0: {
                'Provider': {'code': '20801'},
                'CoverageSite': {'x': '102980'},
                'CoverageType': {'2G': '1'},
            },
        }
        self.assertEqual(result, expected)

    def test_instantiate_models_from_reader(self):
        """
        Tests model instantiation from formatted csv data.
        """
        self.helpers.model_data = {
            0: {
                'Provider': {'code': '20801'},
                'CoverageType': {'2G': '1'},
                'CoverageSite': {'x': '102980', 'y': '6847973'},
            },
        }
        self.helpers.instantiate_models_from_reader()
        # Provider test
        provider = Provider.objects.get(id=1)
        self.assertEqual(provider.name, 'Orange')
        self.assertEqual(provider.ref_code, 20801)
        self.assertEqual(provider.countries[0].name, 'France')
        # Coverage type test
        coverage_type = CoverageType.objects.get(id=1)
        self.assertEqual(coverage_type.name, '2G')
        # Coverage site test
        coverage_site = CoverageSite.objects.get(id=1)
        self.assertEqual(coverage_site.lat, '48.456574558829914')
        self.assertEqual(coverage_site.long, '-5.0888561153013425')
        self.assertEqual(coverage_site.provider.name, 'Orange')
        self.assertEqual(coverage_site.coverage_types.get(pk=coverage_type.pk), coverage_type)

    def test_read_csv_from_url(self):
        """
        Tests URL validations.
        """
        self.helpers.csv_url = 'url_error'
        result = self.helpers.read_csv_from_url()
        self.assertEqual('URL validation error.', result)

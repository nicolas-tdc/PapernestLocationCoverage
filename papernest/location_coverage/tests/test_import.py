"""Test for CSV to database import."""


from django.test import SimpleTestCase
from location_coverage.management.commands._helpers import CsvToDbHelpers


class CSVToDbTest(SimpleTestCase):
    def setUp(self):
        column_field_mapping = {
            'first_column': 'first_field',
            'second_column': 'second_field',
            'third_column': 'third_field',
        }
        self.helpers = CsvToDbHelpers('', {}, column_field_mapping, '')

    def test_map_column_to_fields(self):
        row = {
            'first_column': 'first_value',
            'second_column': 'second_value',
            'third_column': 'third_value',
        }
        mapped_fields = self.helpers.map_columns_to_fields(row)

        expected = {
            'first_field': 'first_value',
            'second_field': 'second_value',
            'third_field': 'third_value',
        }
        self.assertEqual(mapped_fields, expected)

    def test_lambert93_to_gps(self):
        lambert93_coordinates = [
            {'X': '', 'Y': '', 'expected': ('', '')},
            {'X': '', 'Y': '', 'expected': ('', '')},
            {'X': '', 'Y': '', 'expected': ('', '')},
        ]
        for coordinates in lambert93_coordinates:
            result = self.helpers.lambert93_to_gps(coordinates['X'], coordinates['Y'])
            self.assertEqual(result, coordinates['expected'])

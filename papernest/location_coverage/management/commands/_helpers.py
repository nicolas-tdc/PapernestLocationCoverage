"""Helpers for custom manage.py command lines"""


import csv
import urllib.request
import pyproj
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from location_coverage.models import Provider, CoverageSite, CoverageType


class CsvToDbHelpers:
    """
    Helpers for the csv_to_db command line.
    """
    def __init__(self, csv_url, providers_data, csv_model_mapping, csv_delimiter):
        """
        :param csv_url: The URL from which to import CSV data.
        :param providers_data: Mapping for provider code to provider data.
        :param csv_model_mapping: Mapping for csv columns to model fields.
        :param csv_delimiter: Delimiter to parse CSV.
        """
        self.csv_url = csv_url
        self.providers_data = providers_data
        self.csv_model_mapping = csv_model_mapping
        self.csv_delimiter = csv_delimiter
        self.model_data = self.read_csv_from_url()

    def instantiate_models_from_reader(self):
        """
        Creates objects for location coverage models from CSV reader.
        :return: String - Import success or error message.
        """
        if not isinstance(self.model_data, str):
            for row in self.model_data.values():
                # Provider
                provider = Provider.objects.get_or_create(
                    ref_code=row['Provider']['code'], name=self.providers_data[row['Provider']['code']]['name'],
                    countries=self.providers_data[row['Provider']['code']]['country'],
                )
                # Coverage Type
                available_coverage = []
                for coverage_type, available in row['CoverageType'].items():
                    if available == '1':
                        available_type = CoverageType.objects.get_or_create(name=coverage_type)
                        available_coverage.append(available_type[0])
                # Coverage site
                if row['CoverageSite']['x'].isdigit() and row['CoverageSite']['y'].isdigit():
                    long_lat = self.lambert93_to_gps(row['CoverageSite']['x'], row['CoverageSite']['y'])
                    coverage_site = CoverageSite.objects.get_or_create(
                        long=str(long_lat[0]).replace(',', '.'), lat=str(long_lat[1]).replace(',', '.'),
                        provider=provider[0],
                    )
                    coverage_site[0].coverage_types.add(*available_coverage)

            return 'CSV successfully imported.'
        else:
            return self.model_data

    def read_csv_from_url(self):
        """
        Read CSV from url.
        :return: Dict or error message.
        """
        validate = URLValidator()

        try:
            validate(self.csv_url)
            response = urllib.request.urlopen(self.csv_url)

            try:
                # CSV to formatted data
                lines = [line.decode('utf-8') for line in response.readlines()]
                reader = csv.DictReader(lines, delimiter=self.csv_delimiter)
                return self.csv_data_formatter(reader)

            except csv.Error:
                return 'CSV validation error.'

        except ValidationError:
            return 'URL validation error.'

    def csv_data_formatter(self, reader):
        """
        Format data from CSV DictReader for model instantiation.
        :param reader:
        :return: Dict.
        """
        model_data = {}

        for index, row in enumerate(reader):
            model_data[index] = {}
            row_items = self.map_columns_to_fields(row).items()

            for key, value in row_items:
                # Split model and field name
                model_and_field = key.split('__')

                # Add or create model and field entry
                if model_and_field[0] in model_data[index]:
                    model_data[index][model_and_field[0]][model_and_field[1]] = value
                else:
                    model_data[index][model_and_field[0]] = {model_and_field[1]: value}

        return model_data

    def map_columns_to_fields(self, row):
        """
        Map CSV columns to models and fields.
        :param row: CSV row to be mapped.
        :return: Dict.
        """
        mapped_data = {}

        for key, value in row.items():
            if key in self.csv_model_mapping:
                mapped_data[self.csv_model_mapping[key]] = value

        return mapped_data

    @staticmethod
    def lambert93_to_gps(x, y):
        """
        Convert lambert93 coordinates to GPS longitude and latitude.
        :param x: lambert93 x coordinate.
        :param y: lambert93 y coordinate.
        :return: Set.
        """
        lambert = pyproj.Proj(
            '+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000'
            ' +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
        )
        wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        long, lat = pyproj.transform(lambert, wgs84, x, y)

        return long, lat

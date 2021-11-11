"""Helpers for custom manage.py command lines"""


import csv


def read_csv():
    """
    Format data from CSV for model instantiation
    """
    # Read CSV from URL
    with open('REPLACE.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # List by model
        return [map_rows_to_fields(row) for row in reader]


def map_rows_to_fields(row):
    """
    Map CSV rows to model fields
    :param row:
    :return: Dict
    """
    csv_fields_to_model_fields = {
        'Operateur': 'Provider__name',
        'X': 'CoverageSite__x_coordinates',
        'Y': 'CoverageSite__y_coordinates',
        '2G': 'CoverageType__name',
        '3G': 'CoverageType__name',
        '4G': 'CoverageType__name',
    }
    return {
        csv_fields_to_model_fields[key]: value
        for key, value in row.items()
    }


def instantiate_models():
    """
    Instantiate coverage models from CSV formatted data
    """
    model_data = read_csv()
    # Foreach models
    # getattr(models, MODEL_NAME).bulk_create

    MyModel.objects.bulk_create([
        MyModel(**data) for data in model_data
    ])

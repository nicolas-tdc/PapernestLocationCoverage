"""Test for coverage models."""


from django.test import TestCase
from location_coverage.models import Provider, CoverageSite, CoverageType


class ProviderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Provider.objects.create(name="Orange", ref_code="20801", countries='FR')

    def test_name_label(self):
        provider = Provider.objects.get(id=1)
        field_label = provider._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        provider = Provider.objects.get(id=1)
        max_length = provider._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_ref_code_label(self):
        provider = Provider.objects.get(id=1)
        field_label = provider._meta.get_field('ref_code').verbose_name
        self.assertEqual(field_label, 'ref code')

    def test_countries_label(self):
        provider = Provider.objects.get(id=1)
        field_label = provider._meta.get_field('countries').verbose_name
        self.assertEqual(field_label, 'countries')


class CoverageTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CoverageType.objects.create(name="2G")

    def test_name_label(self):
        coverage_type = CoverageType.objects.get(id=1)
        field_label = coverage_type._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        coverage_type = CoverageType.objects.get(id=1)
        max_length = coverage_type._meta.get_field('name').max_length
        self.assertEqual(max_length, 2)


class CoverageSiteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        orange = Provider.objects.create(name="Orange", ref_code="20801", countries='France')
        CoverageSite.objects.create(lat="48.898640", long="2.378260", provider=orange)

    def test_lat_label(self):
        coverage_site = CoverageSite.objects.get(id=1)
        field_label = coverage_site._meta.get_field('lat').verbose_name
        self.assertEqual(field_label, 'lat')

    def test_lat_max_length(self):
        coverage_site = CoverageSite.objects.get(id=1)
        max_length = coverage_site._meta.get_field('lat').max_length
        self.assertEqual(max_length, 19)

    def test_long_label(self):
        coverage_site = CoverageSite.objects.get(id=1)
        field_label = coverage_site._meta.get_field('long').verbose_name
        self.assertEqual(field_label, 'long')

    def test_long_max_length(self):
        coverage_site = CoverageSite.objects.get(id=1)
        max_length = coverage_site._meta.get_field('long').max_length
        self.assertEqual(max_length, 19)

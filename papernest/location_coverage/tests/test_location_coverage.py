"""Tests for CSV to database import."""


from django.test import TestCase

from location_coverage._helpers import LocationCoverageHelpers
from location_coverage.models import Provider, CoverageType, CoverageSite


class LocationCoverageTest(TestCase):
    """
    Tests for location coverage helpers.
    """
    def setUp(self):
        """
        Set up location coverage helpers for testing.
        """
        self.valid_address_helpers = LocationCoverageHelpers('157+boulevard+MacDonald+Paris+75019+France')
        self.invalid_address_helpers = LocationCoverageHelpers('42+rue+papernest+75011+Paris')

    def test_coordinates_from_address(self):
        """
        Tests converting an address to GPS latitude and longitude.
        """
        self.assertEqual(self.valid_address_helpers.coordinates_from_address(), [48.8983508, 2.3778904])
        self.assertEqual(self.invalid_address_helpers.coordinates_from_address(), 'Invalid address.')

    def test_closest_coverage_sites(self):
        """
        Tests finding closest coverage sites from given coordinates.
        """
        self.assertEqual(self.valid_address_helpers.closest_coverage_sites(), 'No coverage site available.')
        self.assertEqual(self.invalid_address_helpers.closest_coverage_sites(), 'Invalid address.')

        # Create a close coverage site.
        orange = Provider.objects.create(name="Orange", ref_code="20801", countries='FR')
        coverage_type_1 = CoverageType.objects.create(name="2G")
        coverage_site = CoverageSite.objects.create(lat="48.89572811690069", long="2.3878872706728376", provider=orange)
        coverage_site.coverage_types.add(coverage_type_1)
        self.assertTrue(type(self.valid_address_helpers.closest_coverage_sites()) is tuple)
        self.assertTrue(self.valid_address_helpers.closest_coverage_sites())

    def test_providers_coverage(self):
        """
        Tests getting providers coverage for closest coverage sites.
        """
        self.assertEqual(self.valid_address_helpers.providers_coverage(), 'No coverage site available.')
        self.assertEqual(self.invalid_address_helpers.providers_coverage(), 'Invalid address.')

        # Create far away coverage site.
        orange = Provider.objects.create(name="Orange", ref_code="20801", countries='FR')
        coverage_type = CoverageType.objects.create(name="2G")
        coverage_site = CoverageSite.objects.create(lat="48.729771273042154", long="2.3632344078211798", provider=orange)
        coverage_site.coverage_types.add(coverage_type)
        self.assertEqual(self.valid_address_helpers.providers_coverage(), 'No close coverage site found.')

        # Create first close coverage site.
        orange = Provider.objects.create(name="Orange", ref_code="20801", countries='FR')
        coverage_type_1 = CoverageType.objects.create(name="2G")
        coverage_site = CoverageSite.objects.create(lat="48.89572811690069", long="2.3878872706728376", provider=orange)
        coverage_site.coverage_types.add(coverage_type_1)
        # Create second close coverage site
        sfr = Provider.objects.create(name="SFR", ref_code="20810", countries='FR')
        coverage_type_2 = CoverageType.objects.create(name="3G")
        coverage_site = CoverageSite.objects.create(lat="48.88572811690069", long="2.3778872706728376", provider=sfr)
        coverage_site.coverage_types.add(coverage_type_1)
        coverage_site.coverage_types.add(coverage_type_2)
        self.assertEqual(
            self.valid_address_helpers.providers_coverage(),
            {'Orange': {'2G': True, '3G': False}, 'SFR': {'2G': True, '3G': True}}
        )

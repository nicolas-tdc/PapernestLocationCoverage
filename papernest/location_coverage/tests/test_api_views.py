"""Tests for API views."""


from rest_framework.test import APITestCase
from rest_framework import status

from location_coverage.models import Provider, CoverageType, CoverageSite


class LocationCoverageAPITests(APITestCase):
    """
    Tests the location coverage main API View.
    """
    def setUp(self):
        self.retrieve_url = '/location-coverage/?q='
        self.valid_address = '157+boulevard+MacDonald+Paris+75019+France'
        self.invalid_address = '42+rue+papernest+75011+Paris'

    def test_invalid_address(self):
        """
        Tests invalid address.
        """
        response = self.client.get(self.retrieve_url + self.invalid_address, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ['Invalid address.'])

    def test_no_site_available(self):
        """
        Tests the case where no coverage site is found in database.
        """
        response = self.client.get(self.retrieve_url + self.valid_address, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ['No coverage site available.'])

    def test_no_close_site_found(self):
        """
        Tests the case where no coverage site was found close enough to the given address.
        """
        # Create a far away coverage site.
        orange = Provider.objects.create(name="Orange", ref_code="20801", countries='FR')
        coverage_type = CoverageType.objects.create(name="2G")
        coverage_site = CoverageSite.objects.create(lat="48.729771273042154", long="2.3632344078211798", provider=orange)
        coverage_site.coverage_types.add(coverage_type)

        response = self.client.get(self.retrieve_url + self.valid_address, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ['No close coverage site found.'])

    def test_close_sites_found(self):
        """
        Tests a successfully retrieved coverage for the given address.
        """
        # Create first close coverage site.
        orange = Provider.objects.create(name="Orange", ref_code="20801", countries='FR')
        coverage_type_1 = CoverageType.objects.create(name="2G")
        coverage_site = CoverageSite.objects.create(lat="48.89572811690069", long="2.3878872706728376", provider=orange)
        coverage_site.coverage_types.add(coverage_type_1)

        # Create second close coverage site.
        sfr = Provider.objects.create(name="SFR", ref_code="20810", countries='FR')
        coverage_type_2 = CoverageType.objects.create(name="3G")
        coverage_site = CoverageSite.objects.create(lat="48.88572811690069", long="2.3778872706728376", provider=sfr)
        coverage_site.coverage_types.add(coverage_type_1)
        coverage_site.coverage_types.add(coverage_type_2)

        response = self.client.get(self.retrieve_url + self.valid_address, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'Orange': {'2G': True, '3G': False}, 'SFR': {'2G': True, '3G': True}}])

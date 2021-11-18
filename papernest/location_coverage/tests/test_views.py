"""Tests for API views."""


from rest_framework.test import APITestCase
from rest_framework import status
from location_coverage.models import Provider, CoverageType, CoverageSite


class LocationCoverageTests(APITestCase):
    def setUp(self):
        self.retrieve_url = '/location-coverage/?q=157+boulevard+MacDonald+Paris+75019+France'

    def test_no_site_available(self):
        response = self.client.get(self.retrieve_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ['No coverage site available.'])

    def test_no_close_site_found(self):
        orange = Provider.objects.create(name="Orange", ref_code="20801", countries='FR')
        coverage_type = CoverageType.objects.create(name="2G")
        coverage_site = CoverageSite.objects.create(lat="48.729771273042154", long="2.3632344078211798", provider=orange)
        coverage_site.coverage_types.add(coverage_type)

        response = self.client.get(self.retrieve_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ['No close coverage site found.'])

    def test_site_found(self):
        orange = Provider.objects.create(name="Orange", ref_code="20801", countries='FR')
        coverage_type = CoverageType.objects.create(name="2G")
        coverage_site = CoverageSite.objects.create(lat="48.89572811690069", long="2.3878872706728376", provider=orange)
        coverage_site.coverage_types.add(coverage_type)

        response = self.client.get(self.retrieve_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'Orange': {'2G': True}}])

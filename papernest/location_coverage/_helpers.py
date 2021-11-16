"""Helpers for location coverage app"""

from django.db.models import Prefetch
from geopy.geocoders import Nominatim
from scipy import spatial
from .models import CoverageSite, CoverageType


class LocationCoverageHelpers:
    def __init__(self, address):
        self.address = address
        self.coordinates = self.geopy_coordinates_from_address()
        pass

    def geopy_coordinates_from_address(self):
        """
        :return: Set - Coordinates for a given address or raise ValueError if address not found
        """
        geolocator = Nominatim(user_agent="papernest")

        location = geolocator.geocode(self.address)
        if location:
            return [location.latitude, location.longitude]
        else:
            raise ValueError('Unknown address.')

    def closest_coverage_sites(self):
        coverage_sites = list(CoverageSite.objects.order_by('id').values_list('lat', 'long'))
        tree = spatial.KDTree(coverage_sites)
        distance, closest_indexes = tree.query([self.coordinates], k=20)
        return distance, closest_indexes

    def providers_coverage(self):
        providers = {}
        coverage_sites = self.closest_coverage_sites()
        for key, coverage_id in enumerate(coverage_sites[1][0]):
            if coverage_sites[0][0][key] < 0.04:
                coverage_site = CoverageSite.objects.get(pk=coverage_id)
                if coverage_site.provider.name not in providers:
                    coverage_types = {cv: False for cv in CoverageType.objects.values_list('name', flat=True)}
                    available_types = coverage_site.coverage_types.values_list('name')
                    for available in available_types:
                        coverage_types[available[0]] = True
                    providers[coverage_site.provider.name] = coverage_types
            else:
                return 'No close coverage site found.'

        return providers

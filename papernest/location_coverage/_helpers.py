"""Helpers for location coverage app"""


from geopy.geocoders import Nominatim
from scipy import spatial
from .models import CoverageSite


class LocationCoverageHelpers():
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

    def coverage_by_site_id(self):
        coverage = {}
        coverage_sites = self.closest_coverage_site()
        for coverage_id in coverage_sites[1]:
            coverage_site = CoverageSite.objects.get(pk=coverage_id)
            for name in coverage_site.name.all() not in coverage:
                pass

"""Helpers for location coverage app."""


from geopy.geocoders import Nominatim
from scipy import spatial
from .models import CoverageSite, CoverageType


class LocationCoverageHelpers:
    def __init__(self, address):
        self.address = address

    def coordinates_from_address(self):
        """
        :return: Set - Latitude and longitude for a given address or raise ValueError if address not found.
        """
        geolocator = Nominatim(user_agent="papernest")
        location = geolocator.geocode(self.address)
        if location:
            return [location.latitude, location.longitude]
        else:
            raise ValueError('Unknown address.')

    def closest_coverage_sites(self):
        """
        :return: Set of 20 closest coverage sites ids with distances to given coordinates.
        """
        coverage_sites = list(CoverageSite.objects.order_by('id').values_list('lat', 'long'))
        tree = spatial.KDTree(coverage_sites)
        return tree.query([self.coordinates_from_address()], k=20)

    def providers_coverage(self):
        """
        :return: Providers coverage for closest coverage sites if close enough.
        """
        providers = {}
        coverage_sites = self.closest_coverage_sites()

        for key, coverage_id in enumerate(coverage_sites[1][0]):
            # Iterate through coverage sites if close enough.
            if coverage_sites[0][0][key] < 0.04:
                coverage_site = CoverageSite.objects.get(pk=coverage_id)
                # Check if close provider has already been found.
                if coverage_site.provider.name not in providers:
                    coverage_types = {cv: False for cv in CoverageType.objects.values_list('name', flat=True)}
                    # Get and add available coverage types to close providers.
                    available_types = coverage_site.coverage_types.values_list('name')
                    for available in available_types:
                        coverage_types[available[0]] = True
                    providers[coverage_site.provider.name] = coverage_types
            else:
                return 'No close coverage site found.'

        return providers

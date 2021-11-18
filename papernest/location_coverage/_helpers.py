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
        if coverage_sites:
            tree = spatial.KDTree(coverage_sites)
            return tree.query([self.coordinates_from_address()], k=20)
        else:
            return False

    def providers_coverage(self):
        """
        :return: Providers coverage for closest coverage sites if close enough.
        """
        providers = {}
        coverage_sites = self.closest_coverage_sites()
        if coverage_sites:
            # Iterate through sites found
            for key, coverage_id in enumerate(coverage_sites[1][0]):
                # Check distances from address
                if coverage_sites[0][0][0] < 0.04:
                    if coverage_sites[0][0][key] < 0.04:
                        coverage_site = CoverageSite.objects.get(pk=coverage_id + 1)
                        # Check if close provider has already been found.
                        if coverage_site.provider.name not in providers:
                            coverage_types = {cv: False for cv in CoverageType.objects.values_list('name', flat=True)}
                            # Get and add available coverage types to close providers.
                            available_types = coverage_site.coverage_types.values_list('name')
                            for available in available_types:
                                coverage_types[available[0]] = True
                            providers[coverage_site.provider.name] = coverage_types
                else:
                    providers = 'No close coverage site found.'

        else:
            providers = 'No coverage site available.'

        return providers

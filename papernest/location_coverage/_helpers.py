"""Helpers for location coverage app."""


from geopy.geocoders import Nominatim
from scipy import spatial

from location_coverage.models import CoverageSite, CoverageType


class LocationCoverageHelpers:
    def __init__(self, address):
        self.address = address
        self.allowed_max_distance = 0.04
        self.number_of_sites_to_retrieve = 20

    def coordinates_from_address(self):
        """
        :return: Set - Latitude and longitude for a given address or raise ValueError if address not found.
        """
        geolocator = Nominatim(user_agent="papernest")
        location = geolocator.geocode(self.address)
        if location:
            return [location.latitude, location.longitude]
        else:
            return 'Invalid address.'

    def closest_coverage_sites(self):
        """
        :return: Set - *number_of_sites_to_retrieve* closest coverage sites ids to given coordinates with distances.
        """
        coverage_sites = list(CoverageSite.objects.order_by('id').values_list('lat', 'long'))
        # Invalid address message.
        if isinstance(self.coordinates_from_address(), str):
            return self.coordinates_from_address()
        # Get closest sites from valid address.
        elif coverage_sites:
            tree = spatial.KDTree(coverage_sites)
            return tree.query([self.coordinates_from_address()], k=self.number_of_sites_to_retrieve)
        # No coverage site in database
        else:
            return 'No coverage site available.'

    def providers_coverage(self):
        """
        :return: Providers coverage for closest coverage sites if closer than *allowed_max_distance*.
        """
        providers = {}
        coverage_sites = self.closest_coverage_sites()

        # Invalid address or no coverage site messages.
        if isinstance(coverage_sites, str):
            return coverage_sites
        else:
            # Iterate through closest found sites.
            for key, coverage_site_id in enumerate(coverage_sites[1][0]):

                # Check distances from address for closest site and current site.
                if coverage_sites[0][0][0] < self.allowed_max_distance:
                    if coverage_sites[0][0][key] < self.allowed_max_distance:
                        coverage_site = CoverageSite.objects.get(pk=coverage_site_id + 1)

                        # Check if close site provider has already been found.
                        if coverage_site.provider.name not in providers:
                            # Get and add available coverage types to close providers.
                            coverage_types = {cv: False for cv in CoverageType.objects.values_list('name', flat=True)}
                            available_types = coverage_site.coverage_types.values_list('name')
                            for available in available_types:
                                coverage_types[available[0]] = True
                            providers[coverage_site.provider.name] = coverage_types
                else:
                    providers = 'No close coverage site found.'

        return providers

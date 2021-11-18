"""API Serializers for Location Coverage App."""


from rest_framework import serializers

from location_coverage.models import Provider, CoverageSite, CoverageType


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    """
    API Serializer for mobile coverage providers.
    """
    class Meta:
        model = Provider
        fields = ['name', 'ref_code']


class CoverageTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    API Serializer for coverage types.
    """
    class Meta:
        model = CoverageType
        fields = ['name']


class CoverageSiteSerializer(serializers.HyperlinkedModelSerializer):
    """
    API Serializer for coverage sites.
    """
    class Meta:
        model = CoverageSite
        fields = ['lat', 'long', 'provider', 'coverage_types']

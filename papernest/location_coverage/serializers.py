"""API Serializers for Location Coverage App."""


from rest_framework import serializers
from .models import Provider, CoverageSite, CoverageType


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    """
    API Serializer for mobile coverage providers.
    """
    model = Provider
    fields = ['name', 'ref_code', 'countries']


class CoverageTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    API Serializer for coverage types.
    """
    model = CoverageType
    fields = ['name']


class CoverageSiteSerializer(serializers.HyperlinkedModelSerializer):
    """
    API Serializer for coverage sites.
    """
    model = CoverageSite
    fields = ['x_coordinates', 'y_coordinates', 'provider', 'coverage_types']

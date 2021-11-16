"""Views for Location Coverage App."""


from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Provider, CoverageSite, CoverageType
from ._helpers import LocationCoverageHelpers
from .serializers import (
    ProviderSerializer, CoverageSiteSerializer, CoverageTypeSerializer
)


"""
Models View Sets.
"""


class ProviderViewSet(viewsets.ModelViewSet):
    """
    View to list or edit coverage providers.

    * Only authenticated users are able to access this view.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [permissions.IsAuthenticated]


class CoverageSiteViewSet(viewsets.ModelViewSet):
    """
    View to list or edit coverage sites.

    * Only authenticated users are able to access this view.
    """
    queryset = CoverageSite.objects.all()
    serializer_class = CoverageSiteSerializer
    permission_classes = [permissions.IsAuthenticated]


class CoverageTypeViewSet(viewsets.ModelViewSet):
    """
    View to list or edit coverage types.

    * Only authenticated users are able to access this view.
    """
    queryset = CoverageType.objects.all()
    serializer_class = CoverageTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


"""
Custom API Views.
"""


@api_view(['GET'])
def location_coverage(request):
    """
    :param request:
    :return: View listing coverage by provider for a given address sent as a GET URL parameter.
    """
    address = request.GET.get('q')
    helpers = LocationCoverageHelpers(address)
    return Response([helpers.providers_coverage()])

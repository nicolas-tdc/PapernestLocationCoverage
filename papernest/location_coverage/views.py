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


@api_view(['GET'])
def location_coverage(request):
    available_coverage = []
    address = request.GET['q']
    helpers = LocationCoverageHelpers(address)
    # for available in helpers.coverage_by_site_id().all():
    #     available_coverage.append(available)
    # for poll in Poll.objects.all():
    #     for choice in poll.choice.all():
    return Response({'coverage': helpers.closest_coverage_sites()})

"""Views for Location Coverage App."""


from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Provider, CoverageSite, CoverageType
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


# class LocationCoverage(APIView):
#     """
#     View to get providers' mobile coverage for a given address.
#
#     * Only authenticated users are able to access this view.
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request):
#         """
#         Return a list of providers with available coverage.
#         """
#         pass
#         # return Response(coverage)
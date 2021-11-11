"""URL and routes configurations for Location Coverage App"""


from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from location_coverage.views import (
    ProviderViewSet, CoverageSiteViewSet, CoverageTypeViewSet,
    # LocationCoverageViewSet
)


"""
ViewSets Routing.
"""
router = routers.DefaultRouter()
router.register(r'providers', ProviderViewSet)
router.register(r'coverage-sites', CoverageSiteViewSet)
router.register(r'coverage-types', CoverageTypeViewSet)
# router.register(r'', LocationCoverageViewSet)


"""
URL Patterns.
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]

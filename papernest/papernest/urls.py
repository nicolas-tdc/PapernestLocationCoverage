"""URL and routes configurations for Location Coverage App"""


from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from location_coverage import views


"""
ViewSets Routing.
"""

router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'coverage-sites', views.CoverageSiteViewSet)
router.register(r'coverage-types', views.CoverageTypeViewSet)


"""
URL Patterns.
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('location-coverage/', views.location_coverage),
]

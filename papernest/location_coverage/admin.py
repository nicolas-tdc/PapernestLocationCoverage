"""Admin settings for location coverage app"""


from django.contrib import admin
from .models import Provider, CoverageSite, CoverageType


# Register models in admin.
admin.site.register(Provider)
admin.site.register(CoverageSite)
admin.site.register(CoverageType)

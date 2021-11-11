from django.contrib import admin
from .models import Provider, CoverageSite, CoverageType


admin.site.register(Provider)
admin.site.register(CoverageSite)
admin.site.register(CoverageType)

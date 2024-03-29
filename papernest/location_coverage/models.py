"""Models for Location Coverage App."""


from django.db import models
from django_countries.fields import CountryField


class Provider(models.Model):
    """
    Model for mobile coverage provider.
    """
    name = models.CharField(max_length=100)
    ref_code = models.IntegerField()
    countries = CountryField(multiple=True)


class CoverageType(models.Model):
    """
    Model for coverage type attached to a coverage site.
    """
    name = models.CharField(max_length=2)


class CoverageSite(models.Model):
    """
    Model for coverage site with coordinates attached to a provider.
    """
    lat = models.CharField(max_length=19)
    long = models.CharField(max_length=19)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    coverage_types = models.ManyToManyField(CoverageType, related_name='coverage_types')

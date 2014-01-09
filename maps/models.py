import os

from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User

class Map(geomodels.Model):
    """Map object"""
    title = models.CharField(max_length=128, unique=True)
    date = models.DateField()
    theme = models.ForeignKey('Theme')
    category = models.ForeignKey('Category')
    source = models.ForeignKey('Source')
    description = models.TextField(blank=True, null=True)
    scale = models.CharField(max_length=20, blank=True, null=True)
    request = models.ForeignKey('MapRequest')
    map_file = models.FileField(upload_to='uploads/maps')
    map_thumbnail = models.FileField(upload_to='uploads/thumbnails',  blank=True, null=True)
    center = geomodels.PointField(blank=True, null=True)
    country = models.ForeignKey('Country')
    size = models.ForeignKey('MapSize', blank=True, null=True)

    def __unicode__(self):
        return self.title

class Theme(models.Model):
    """Theme object"""
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

class MapRequest(models.Model):
    """Request for a map"""
    title = models.CharField(max_length=128)
    email = models.EmailField()
    user = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    purpose = models.TextField(blank=True, null=True)
    extended_description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    size = models.ForeignKey('MapSize')
    format = models.ForeignKey('Format')
    requester = models.ForeignKey('Requester')

    def __unicode__(self):
        return self.title

class Country(models.Model):
    """Country object"""
    fips = models.CharField('FIPS', max_length=5, unique=True)
    name = models.CharField(max_length=128, unique=True)
    iso2 = models.CharField(max_length=2, blank=True, null=True, unique=True)
    iso3 = models.CharField(max_length=3, blank=True, null=True, unique=True)
    countries = models.ManyToManyField('Country', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return self.name

class Format(models.Model):
    """Format object"""
    name = models.CharField(max_length=20)
    resolution = models.CharField(max_length=10, choices=[['high','High'],['low','Low']])

    class Meta:
        unique_together = ('name', 'resolution')

    def __unicode__(self):
        return "%s - %s" % (self.name, self.resolution)

class MapSize(models.Model):
    """Map Sizes"""
    name = models.CharField(max_length=5, unique=True)
    dimensions = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Category(models.Model):
    """Category object"""
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

class Requester(models.Model):
    """Who requests for a map"""
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

class Source(models.Model):
    """Data source"""
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name
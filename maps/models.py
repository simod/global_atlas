import os
import datetime

from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Count

class CountryManager(models.Manager):
    """Custom Country model manager"""

    def get_countries(self):
        """Return just the unrelated countries"""
        return Country.objects.annotate(Count('countries')) \
            .filter(countries__count=0)

    def get_regions(self):
        """Return just the related countries"""
        return Country.objects.annotate(Count('countries')) \
            .filter(fips__regex=r'^.{3,}$')

class Map(geomodels.Model):
    """Map object"""
    title = models.CharField(max_length=255)
    date = models.DateField()
    theme = models.ForeignKey('Theme')
    category = models.ForeignKey('Category')
    source = models.ForeignKey('Source')
    description = models.TextField(blank=True, null=True, default="No description given")
    scale = models.CharField(max_length=20, blank=True, null=True)
    request = models.ForeignKey('MapRequest')
    map_file = models.FileField(upload_to='maps')
    map_thumbnail = models.FileField(upload_to='thumbnails',  blank=True, null=True)
    country = models.ForeignKey('Country')
    size = models.ForeignKey('MapSize')
    center = geomodels.PointField(blank=True, null=True)
    
    def __unicode__(self):
        return self.title

class Theme(models.Model):
    """Theme object"""
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super(Theme, self).save(*args, **kwargs)

class MapRequest(models.Model):
    """Request for a map"""
    title = models.CharField(max_length=128)
    email = models.EmailField()
    user = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    purpose = models.TextField(blank=True, null=True)
    extended_description = models.TextField('Description', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    deadline = models.DateField(default=datetime.date(year=2015, month=12, day=31))
    size = models.ForeignKey('MapSize')
    format = models.ForeignKey('Format')
    requester = models.ForeignKey('Requester', verbose_name='Institution')

    def __unicode__(self):
        return self.title

class Country(geomodels.Model):
    """Country object"""
    fips = models.CharField('FIPS', max_length=5, unique=True)
    name = models.CharField(max_length=128, unique=True)
    iso2 = models.CharField(max_length=2, blank=True, null=True)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    geometry = geomodels.MultiPolygonField(blank=True, null=True)
    countries = models.ManyToManyField('Country', blank=True, null=True, related_name='subcountries')

    objects = CountryManager()

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
    name = models.CharField(max_length=15, unique=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super(Category, self).save(*args, **kwargs)

class Requester(models.Model):
    """Who requests for a map"""
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super(Requester, self).save(*args, **kwargs)

class Source(models.Model):
    """Data source"""
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super(Source, self).save(*args, **kwargs)


class CollinsMap(models.Model):
    """Collins maps"""
    name = models.CharField(max_length=128)
    the_file = models.FileField(upload_to='collins')
    country = models.ForeignKey('Country')

    def __unicode__(self):
        return self.name
        
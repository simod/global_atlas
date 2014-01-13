import os

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
            .filter(countries__count__gt=0)

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
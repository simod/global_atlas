import json

from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Count
from django.http import HttpResponse

from .forms import MapRequestValidationForm
from .models import Country, Category, Theme, Map

class Home(View):
    """Render home page"""

    form_class = MapRequestValidationForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(form_name='mr_form')
        return render(request, self.template_name, {
                'mr_form': form,
                'countries': Country.objects.get_countries(),
                'regions': Country.objects.get_regions().annotate(maps_count=Count('map')), 
                'categories': Category.objects.annotate(maps_count=Count('map')),
                'themes': Theme.objects.all()
            })
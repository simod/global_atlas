from django.shortcuts import render
from django.views.generic.base import View

from .forms import MapRequestValidationForm
from .models import Country, Category, Theme

class Home(View):
    """Render home page"""

    form_class = MapRequestValidationForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(form_name='mr_form')
        return render(request, self.template_name, {
                'mr_form': form,
                'countries': Country.objects.get_countries(),
                'regions': Country.objects.get_regions(), 
                'categories': Category.objects.all(),
                'themes': Theme.objects.all()
            })
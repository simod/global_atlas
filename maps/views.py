from django.shortcuts import render
from django.views.generic.base import View

from .forms import MapRequestForm

class Home(View):
    """Render home page"""

    form_class = MapRequestForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'mr_form': form})
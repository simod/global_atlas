from django.forms import ModelForm
from djangular.forms import NgModelFormMixin, NgFormValidationMixin

from .models import MapRequest


class MapRequestForm(ModelForm):
    """Form for the map request model"""

    class Meta:
        model = MapRequest
        fields = [
            'title',
            'email',
            'purpose',
            'extended_description',
            'content',
            'deadline',
            'size',
            'format',
            'requester'
        ]


class MapRequestValidationForm(NgModelFormMixin, NgFormValidationMixin, MapRequestForm):
    """Form for the map request model"""

    pass
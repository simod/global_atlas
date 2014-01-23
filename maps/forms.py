from django.forms import ModelForm
from djangular.forms.angular_model import NgModelFormMixin

from .models import MapRequest


class MapRequestForm(NgModelFormMixin, ModelForm):
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
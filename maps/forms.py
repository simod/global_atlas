from django.forms import ModelForm
from djangular.forms import NgModelFormMixin, NgFormValidationMixin, AddPlaceholderFormMixin

from .models import MapRequest


class MapRequestForm(ModelForm):
    """Form for the map request model, used in the apis"""

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
            'requester',
            'quantity',
        ]

    def __init__(self, *args, **kwargs):
        super(MapRequestForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'pull-right'

class MapRequestValidationForm(AddPlaceholderFormMixin, 
    NgModelFormMixin, NgFormValidationMixin, MapRequestForm):
    """Form use on the client side, adds validation fields"""

    pass
    
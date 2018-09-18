from django.forms import ModelForm

from .models import *


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class ProjectForm(ModelForm):
    class Meta:
        model = ProjectNew
        fields = '__all__'


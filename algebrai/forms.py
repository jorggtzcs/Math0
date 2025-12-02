from django import forms
from .models import Classroom


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'description']


class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=10, label="Class Code")

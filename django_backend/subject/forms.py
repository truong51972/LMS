from django import forms
from .models import Subject

# Form for creating and editing subjects
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']

from django import forms
from .models import Material

class MaterialUploadForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['subject', 'material_type', 'file']

    material_type = forms.ChoiceField(choices=Material.MATERIAL_TYPE_CHOICES, widget=forms.RadioSelect)


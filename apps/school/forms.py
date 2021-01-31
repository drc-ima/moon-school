from django import forms

from apps.pupil.models import Pupil, Class


class PupilForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        school_id = kwargs.pop('school_id')
        super(PupilForm, self).__init__(*args, **kwargs)
        self.fields['classs'].queryset = Class.objects.filter(school_id=school_id)
        self.fields['classs'].label = 'Class'
    class Meta:
        model = Pupil
        fields = ('pupil_id', 'first_name', 'middle_name', 'last_name', 'classs', 'previous_school',
                  'date_of_birth', 'guardian', 'mother_name', 'father_name', 'guardian_contact', 'address',
                  'profile', 'gender')
        widgets = {
            'pupil_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pupil ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Last Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'classs': forms.Select(attrs={'class': 'custom-select', 'required': True}),
            'previous_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Previous School'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guardian': forms.Select(attrs={'class': 'custom-select', 'required': True}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Father Name'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mother Name'}),
            'guardian_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guardian Contact'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Home Address'}),
            'gender': forms.Select(attrs={'class': 'custom-select', 'required': True}),
            'profile': forms.FileInput(attrs={'class': 'form-control'})
        }

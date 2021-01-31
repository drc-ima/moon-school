from django import forms

from apps.staff.models import Staff


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ('staff_id', 'first_name', 'middle_name', 'gender', 'last_name', 'staff_type', 'date_employed', 'date_of_birth', 'profile')
        widgets = {
            'date_employed': forms.DateInput(attrs={'autocomplete': 'off', 'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Employment'}),
            'date_of_birth': forms.DateInput(attrs={'autocomplete': 'off', 'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Birth'}),
            'profile': forms.FileInput(attrs={'type': 'file', 'class': 'custom-file', 'placeholder': 'Select Image'}),
            'staff_id': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'required': True, 'placeholder': 'Staff ID'}),
            'first_name': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'required': True, 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'required': True, 'placeholder': 'Last Name'}),
            'middle_name': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': 'Middle Name'}),
            'staff_type': forms.Select(attrs={'class': 'custom-select'}),
            'gender': forms.Select(attrs={'class': 'custom-select', 'required': True})
        }

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

        self.fields['staff_type'].choices = {('', 'Choose Staff Category'), ('ASH', 'Assistant School Head'), ('TU', 'Teacher'), ('CT', 'Class Teacher'), ('FO', 'Finance Officer')}
        self.fields['gender'].choices = {('', 'Choose Gender'), ('male', 'Male'), ('female', 'Female')}